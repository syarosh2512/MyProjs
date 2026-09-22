import subprocess

def show_my_network_connections():
    """Show network shares that I am connected to with credentials info and save to file."""
    
    with open('my_network_connections.txt', 'w') as f:
        f.write("=== My Network Drive Connections ===\n")
        try:
            result = subprocess.run('net use', shell=True, capture_output=True, text=True)
            f.write(result.stdout)
        except Exception as e:
            f.write(f"Error getting network connections: {e}\n")
        
        f.write("\n=== Stored Credentials ===\n")
        try:
            result = subprocess.run('cmdkey /list', shell=True, capture_output=True, text=True)
            f.write(result.stdout)
        except Exception as e:
            f.write(f"Error getting stored credentials: {e}\n")
        
        f.write("\n=== Mapped Network Drives ===\n")
        try:
            result = subprocess.run('wmic logicaldisk where drivetype=4 get size,freespace,caption', shell=True, capture_output=True, text=True)
            f.write(result.stdout)
        except Exception as e:
            f.write(f"Error getting mapped drives: {e}\n")
        
        f.write("\n=== Current User Context ===\n")
        try:
            result = subprocess.run('whoami', shell=True, capture_output=True, text=True)
            f.write(f"Running as: {result.stdout.strip()}\n")
        except Exception as e:
            f.write(f"Error getting user context: {e}\n")
    
    print("Network connections information saved to my_network_connections.txt")

if __name__ == "__main__":
    show_my_network_connections()