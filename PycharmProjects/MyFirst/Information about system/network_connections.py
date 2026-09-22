import subprocess

def show_network_connections():
    """Show all network connections on Windows PC and save to file."""
    
    with open('network_info.txt', 'w') as f:
        f.write("=== Active Network Connections ===\n")
        try:
            # Show active TCP/UDP connections
            result = subprocess.run('netstat -an', shell=True, capture_output=True, text=True)
            f.write(result.stdout)
        except Exception as e:
            f.write(f"Error getting connections: {e}\n")
        
        f.write("\n=== Network Interfaces ===\n")
        try:
            # Show network interfaces
            result = subprocess.run('ipconfig', shell=True, capture_output=True, text=True)
            f.write(result.stdout)
        except Exception as e:
            f.write(f"Error getting interfaces: {e}\n")
        
        f.write("\n=== Routing Table ===\n")
        try:
            # Show routing table
            result = subprocess.run('route print', shell=True, capture_output=True, text=True)
            f.write(result.stdout)
        except Exception as e:
            f.write(f"Error getting routes: {e}\n")
    
    print("Network information saved to network_info.txt")

if __name__ == "__main__":
    show_network_connections()