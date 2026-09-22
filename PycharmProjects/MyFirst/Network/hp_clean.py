import paramiko
import time

def get_config(host):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username='admin', password='D62S0071501')
        
        shell = ssh.invoke_shell()
        time.sleep(2)
        shell.recv(4096)
        shell.send('\r\n')
        time.sleep(1)
        shell.recv(1024)
        shell.send('show running-config\r\n')
        time.sleep(1)
        
        output = ''
        for i in range(100):
            if shell.recv_ready():
                data = shell.recv(8192).decode('utf-8', errors='ignore')
                output += data
                if 'Press any key to continue' in data:
                    shell.send(' ')
                elif '# ' in data and len(output) > 1000:
                    break
            time.sleep(0.3)
        
        ssh.close()
        
        with open(f"{host}.txt", 'w') as f:
            f.write(output)
        print(f"✓ {host} - {len(output)} bytes")
    except Exception as e:
        print(f"✗ {host} - {e}")

get_config('10.222.1.56')