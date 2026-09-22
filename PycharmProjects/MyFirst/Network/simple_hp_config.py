import telnetlib

def download_hp_config(host, username, password):
    try:
        tn = telnetlib.Telnet(host, 23, timeout=5)
        tn.read_until(b"Username: ")
        tn.write(username.encode() + b"\r\n")
        tn.read_until(b"Password: ")
        tn.write(password.encode() + b"\r\n")
        tn.read_until(b"> ")
        tn.write(b"show running-config\r\n")
        config = tn.read_until(b"> ", timeout=30).decode()
        tn.write(b"exit\r\n")
        tn.close()
        
        with open(f"{host}_config.txt", 'w') as f:
            f.write(config)
        print(f"✓ {host}")
        return True
    except:
        return False

if __name__ == "__main__":
    for i in range(54, 56):
        download_hp_config(f'10.222.1.{i}', 'admin', 'D62S0071501')