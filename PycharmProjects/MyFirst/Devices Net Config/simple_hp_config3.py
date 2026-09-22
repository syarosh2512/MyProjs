import paramiko
import socket

def download_hp_config(host, username, password, port=22, hp_type='comware'):
    """Download configuration from HP network device using paramiko."""
    
    # Check if port is open first
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
    
    if result != 0:
        return None  # Port not open, skip silently

    # Set command based on HP type
    config_command = 'display current-configuration' if hp_type.lower() == 'comware' else 'show running-config'
    
    ssh = None
    try:
        # Create SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect with minimal parameters
        ssh.connect(host, username=username, password=password, timeout=3)

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
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(config)

        print(f"✓ {host}: Configuration saved to {filename}")
        return filename

    except (paramiko.ssh_exception.SSHException, socket.error):
        return None  # Skip devices with SSH issues
    except Exception:
        return None  # Skip any other errors
    finally:
        if ssh:
            ssh.close()

if __name__ == "__main__":
    credentials = [('d62s0071501', 'D62S0071501'), ('admin', 'D62S0071501'), ('admin', 'admin')]
    
    for i in range(10, 62):
        for username, password in credentials:
            result = download_hp_config(f'10.222.1.{i}', username, password, hp_type='procurve')
            if result:
                break