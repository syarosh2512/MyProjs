
<#
.SYNOPSIS
  SMB connectivity diagnostics to a target host (helps troubleshoot "System error 53 / network path not found").

.PARAMETER Target
  Target computer name or IP address (required).

.PARAMETER Credential
  Credentials for remote access (CIM/WMI/SMB) if needed.

.PARAMETER TimeoutMs
  Timeout (ms) for network checks. Default: 2000.

.EXAMPLE
  .\Test-SmbConnectivity.ps1 -Target 10.221.131.151

.EXAMPLE
  $cred = Get-Credential
  .\Test-SmbConnectivity.ps1 -Target PC-01 -Credential $cred
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$Target,

    [System.Management.Automation.PSCredential]$Credential,

    [int]$TimeoutMs = 2000
)

function Write-Section($title) {
    Write-Host ""
    Write-Host "=== $title ===" -ForegroundColor Cyan
}

function Test-TcpPort {
    param(
        [string]$ComputerName,
        [int[]]$Ports,
        [int]$TimeoutMs = 2000
    )
    foreach ($p in $Ports) {
        try {
            $r = Test-NetConnection -ComputerName $ComputerName -Port $p -WarningAction SilentlyContinue -InformationLevel Quiet
            [pscustomobject]@{
                Computer = $ComputerName
                Port     = $p
                Open     = [bool]$r
            }
        } catch {
            [pscustomobject]@{
                Computer = $ComputerName
                Port     = $p
                Open     = $false
            }
        }
    }
}

function Get-NetworkProfile {
    try {
        Get-NetConnectionProfile | Select-Object InterfaceAlias, NetworkCategory, IPv4Connectivity, IPv6Connectivity
    } catch {
        $null
    }
}

function Get-FirewallSmbState {
    $groups = @(
        "File and Printer Sharing",
        "Network Discovery"
    )
    $rules = foreach ($g in $groups) {
        try {
            Get-NetFirewallRule -DisplayGroup $g -ErrorAction Stop |
            Get-NetFirewallRule | Select-Object -Unique DisplayName, Enabled, Profile, Direction, Action
        } catch {
            $null
        }
    }
    $rules
}

function Get-ServiceState {
    param([string[]]$Names)
    foreach ($n in $Names) {
        try {
            $s = Get-Service -Name $n -ErrorAction Stop
            [pscustomobject]@{ Name=$n; Status=$s.Status; StartType=(Get-WmiObject Win32_Service -Filter "Name='$n'").StartMode }
        } catch {
            [pscustomobject]@{ Name=$n; Status="NotFound"; StartType=$null }
        }
    }
}

function Test-CimShares {
    param([string]$ComputerName,[System.Management.Automation.PSCredential]$Credential,[switch]$IncludeHidden)
    try {
        $cimParams = @{ ComputerName = $ComputerName; ErrorAction='Stop' }
        if ($Credential) { $cimParams.Credential = $Credential }
        $session = New-CimSession @cimParams
        try {
            $shares = Get-SmbShare -CimSession $session -ErrorAction Stop
            if (-not $IncludeHidden) { $shares = $shares | Where-Object { $_.Name -notmatch '\$$' } }
            $ok = $true
            $data = $shares | Select-Object Name, Path, Description, EncryptData, ShareState
        } catch {
            # Fallback to classic WMI
            $shares = Get-WmiObject -Class Win32_Share -ComputerName $ComputerName -ErrorAction Stop
            if (-not $IncludeHidden) { $shares = $shares | Where-Object { $_.Name -notmatch '\$$' } }
            $ok = $true
            $data = $shares | Select-Object Name, Path, Description, Status
        } finally {
            if ($session) { $session | Remove-CimSession }
        }
        [pscustomobject]@{ Success=$ok; Data=$data }
    } catch {
        [pscustomobject]@{ Success=$false; Data=$null; Error=$_.Exception.Message }
    }
}

function Get-SmbConfigSummary {
    $client = $server = $null
    try { $client = Get-SmbClientConfiguration } catch {}
    try { $server = Get-SmbServerConfiguration } catch {}
    [pscustomobject]@{
        Client_DigitallySign      = $client.RequireSecuritySignature
        Client_EncryptData        = $client.EncryptData
        Client_EnableSMB1Protocol = $client.EnableSMB1Protocol
        Client_EnableSMB2Protocol = $client.EnableSMB2Protocol
        Server_EncryptData        = $server.EncryptData
        Server_EnableSMB1Protocol = $server.EnableSMB1Protocol
        Server_SigningRequired    = $server.RequireSecuritySignature
        Server_AuditSmb1Access    = $server.AuditSmb1Access
    }
}

function Test-SmbSessionTry {
    param([string]$ComputerName,[System.Management.Automation.PSCredential]$Credential)
    # Try opening \\host\IPC$ as a lightweight SMB test
    try {
        $path = "\\$ComputerName\IPC$"
        if ($Credential) {
            # Create explicit session
            $domainUser = $Credential.UserName
            $pw = $Credential.GetNetworkCredential().Password
            $null = cmd /c "net use $path /user:$domainUser $pw" 2>$null
        }
        # Check reachability
        $exists = Test-Path $path
        if ($Credential) {
            cmd /c "net use $path /delete /y" | Out-Null
        }
        [pscustomobject]@{ Path=$path; Reachable=$exists }
    } catch {
        [pscustomobject]@{ Path="\\$ComputerName\IPC$"; Reachable=$false; Error=$_.Exception.Message }
    }
}

# ---------------- MAIN ----------------
$summary = [ordered]@{
    Target                = $Target
    Ping                  = $false
    DnsResolved           = $null
    Tcp445_Open           = $false
    Tcp139_Open           = $false
    Local_Services        = $null
    Local_Firewall_OK     = $null
    Local_NetworkProfile  = $null
    Smb_Config            = $null
    Smb_Session_OK        = $false
    Remote_Shares_Queried = $false
    Remote_Shares_Count   = 0
    Remote_Error          = $null
}

Write-Section "Basic network checks"
# DNS
try {
    $dns = Resolve-DnsName -Name $Target -ErrorAction Stop
    $summary.DnsResolved = ($dns | Select-Object -First 1 -ExpandProperty NameHost -ErrorAction SilentlyContinue)
    Write-Host "DNS: records found for $Target" -ForegroundColor Green
} catch {
    Write-Host "DNS: resolution failed (it may be an IP or you may need hosts/DNS)" -ForegroundColor Yellow
}

# Ping
try {
    $ping = Test-Connection -ComputerName $Target -Count 2 -Quiet -ErrorAction SilentlyContinue
    $summary.Ping = [bool]$ping
    if ($summary.Ping) { Write-Host "Ping: responding" -ForegroundColor Green }
    else { Write-Host "Ping: no reply (ICMP might be blocked; not critical for SMB)" -ForegroundColor Yellow }
} catch { }

Write-Section "Check SMB ports (TCP 445/139)"
$ports = Test-TcpPort -ComputerName $Target -Ports 445,139 -TimeoutMs $TimeoutMs
$tcp445 = $ports | Where-Object {$_.Port -eq 445}
$tcp139 = $ports | Where-Object {$_.Port -eq 139}
$summary.Tcp445_Open = $tcp445.Open
$summary.Tcp139_Open = $tcp139.Open
$ports | Format-Table -AutoSize

Write-Section "Local services, network profile, and firewall"
$summary.Local_NetworkProfile = Get-NetworkProfile
$summary.Local_Services = Get-ServiceState -Names @('LanmanWorkstation','LanmanServer','Bowser','FDResPub')
$fw = Get-FirewallSmbState
$summary.Local_Firewall_OK = ($fw | Where-Object { $_.Enabled -eq 'True' -and $_.Action -eq 'Allow' }).Count -gt 0
$summary.Local_Services | Format-Table -AutoSize
if ($summary.Local_NetworkProfile) { $summary.Local_NetworkProfile | Format-Table -AutoSize }
if ($fw) { $fw | Sort-Object DisplayName | Format-Table -AutoSize }

Write-Section "SMB configuration (local client/server)"
$summary.Smb_Config = Get-SmbConfigSummary
$summary.Smb_Config | Format-Table -AutoSize

Write-Section "Attempt SMB session (IPC$)"
$ipc = Test-SmbSessionTry -ComputerName $Target -Credential $Credential
$summary.Smb_Session_OK = $ipc.Reachable
$ipc | Format-Table -AutoSize

Write-Section "Query remote shares"
$sharesResult = Test-CimShares -ComputerName $Target -Credential $Credential
if ($sharesResult.Success) {
    $summary.Remote_Shares_Queried = $true
    $summary.Remote_Shares_Count   = ($sharesResult.Data | Measure-Object).Count
    if ($sharesResult.Data) { $sharesResult.Data | Sort-Object Name | Format-Table -AutoSize }
} else {
    $summary.Remote_Error = $sharesResult.Error
    Write-Warning "Failed to query remote shares: $($sharesResult.Error)"
}

Write-Section "SUMMARY (for System error 53)"
$report = [pscustomobject]$summary
$report | Format-List

Write-Host ""
Write-Host "Interpretation:" -ForegroundColor Magenta
if (-not $summary.Tcp445_Open -and -not $summary.Tcp139_Open) {
    Write-Host " - TCP 445/139 to $Target are closed or unreachable. Check firewall/routing." -ForegroundColor Yellow
}
elseif ($summary.Tcp445_Open -and -not $summary.Smb_Session_OK) {
    Write-Host " - TCP 445 is open, but SMB session did not establish. Possible auth/policy/SMB version mismatch." -ForegroundColor Yellow
}
if ($summary.Remote_Shares_Queried -and $summary.Remote_Shares_Count -eq 0) {
    Write-Host " - Access works, but no published shares (or only hidden). Try with credentials/IncludeHidden." -ForegroundColor Yellow
}
if ($summary.Remote_Error) {
    Write-Host " - Error while querying remote host: $($summary.Remote_Error)" -ForegroundColor Yellow
}
Write-Host "Done." -ForegroundColor Green
10ю210.22