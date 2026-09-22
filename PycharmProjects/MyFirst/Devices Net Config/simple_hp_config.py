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
    
    ssh = None
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
            look_for_keys=False
        )

        # Use interactive shell for HP devices
        shell = ssh.invoke_shell()
        
        # Wait for initial prompt
        import time
        time.sleep(1)
        
        # Clear initial output
        if shell.recv_ready():
            shell.recv(4096)
        
        # Send command
        shell.send(config_command + '\n')
        time.sleep(3)
        
        # Read all output
        config = ''
        while shell.recv_ready():
            config += shell.recv(4096).decode('utf-8')
            time.sleep(0.1)
        
        shell.close()
        
        # Filter out error messages
        if 'SSH command execution is not supported' in config or not config.strip():
            return None

        # Save to file
        filename = f"{host}_hp_config.txt"
        with open(filename, 'w') as f:
            f.write(config)

        print(f"✓ {host}: Configuration saved to {filename}")
        return filename

    except paramiko.ssh_exception.SSHException as e:
        if "Invalid packet blocking" in str(e):
            return None  # Skip devices with invalid packet blocking
        return None  # Skip devices with other SSH issues
    except socket.error:
        return None  # Skip devices with socket issues
    except Exception:
        return None  # Skip any other errors
    finally:
        if ssh:
            ssh.close()

if __name__ == "__main__":
    credentials = [
        ('admin', 'D62S0071501'),
        ('d62s0071501', 'D62S0071501')
    ]

    for i in range(55, 57):
        host = f'10.222.1.{i}'
        for username, password in credentials:
            result = download_hp_config(
                host=host,
                username=username,
                password=password,
                hp_type='procurve'
            )
            if result:
                print(f"Config saved: {result}")
                break  # Success, try next host