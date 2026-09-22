import paramiko
import time

def get_config(host):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username='admin', password='D62S0071501', timeout=5)
        
        shell = ssh.invoke_shell()
        shell.recv(1024)  # Clear welcome
        shell.send('show running-config\n')
        time.sleep(10)
        
        output = shell.recv(65536).decode('utf-8', errors='ignore')
        ssh.close()
        
        with open(f"{host}.txt", 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"✓ {host}")
    except Exception as e:
        print(f"✗ {host} - {e}")

get_config('10.222.1.56')