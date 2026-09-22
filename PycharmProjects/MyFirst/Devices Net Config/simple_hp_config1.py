import paramiko
import socket

def download_hp_config(host, username, password, port=22, hp_type='comware'):
    """Download configuration from HP network device using paramiko."""
    
    # Check if port is open first
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    result = sock.connect_ex((host, port))
    sock.close()
    
    if result != 0:
        return None  # Port not open, skip silently

    # Set command based on HP type
    config_command = 'display current-configuration' if hp_type.lower() == 'comware' else 'show running-config'
    
    try:
        # Create SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to device
        ssh.connect(
            hostname=host,
            username=username,
            password=password,
            port=port,
            timeout=5,
            allow_agent=False,
            look_for_keys=False,
            sock=None,
            gss_auth=False,
            gss_kex=False,
            gss_deleg_creds=False,
            gss_host=None,
            banner_timeout=200,
            auth_timeout=None,
            gss_trust_dns=True,
            passphrase=None,
            disabled_algorithms=None
        )

        # Execute command
        stdin, stdout, stderr = ssh.exec_command(config_command)

        # Get the output
        config = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        if error:
            print(f"Command error: {error}")
            return None

        # Save to file
        filename = f"{host}_hp_config.txt"
        with open(filename, 'w') as f:
            f.write(config)

        print(f"✓ {host}: Configuration saved to {filename}")
        ssh.close()
        return filename

    except (paramiko.ssh_exception.SSHException, socket.error):
        return None  # Skip devices with SSH issues
    except paramiko.ssh_exception.SSHException as e:
        if "Invalid packet blocking" in str(e):
            return None  # Skip devices with invalid packet blocking
        raise
    except Exception:
        return None  # Skip any other errors

if __name__ == "__main__":
    for i in range(2, 251):
        result = download_hp_config(
            host=f'10.222.1.{i}',
            username='admin',
            password='D62S0071501',
            hp_type='procurve'
        )
        if result:
            print(f"Config saved: {result}")
        else:
            # Try with alternative credentials
            result = download_hp_config(
                host=f'10.222.1.{i}',
                username='admin',
                password='admin',
                hp_type='procurve'
