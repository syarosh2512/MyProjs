import subprocess
import socket
import csv
from concurrent.futures import ThreadPoolExecutor

def ping_host(ip):
    """Ping a single host and resolve hostname."""
    try:
        # Ping command for Windows
        result = subprocess.run(['ping', '-n', '1', '-w', '1000', ip], 
                              capture_output=True, text=True)
        is_alive = result.returncode == 0
        
        # Try to resolve hostname
        hostname = 'Unknown'
        if is_alive:
            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except:
                hostname = 'No hostname'
        
        return {
            'ip': ip,
            'status': 'Online' if is_alive else 'Offline',
            'hostname': hostname
        }
    except:
        return {'ip': ip, 'status': 'Error', 'hostname': 'Error'}

def scan_network():
    """Scan 192.168.0.0/24 network."""
    print("Scanning network 10.221.131.0/24...")
    
    # Generate IP list
    ips = [f"10.221.131.{i}" for i in range(1, 255)]
    
    results = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(ping_host, ips))
    
    # Filter only online hosts
    online_hosts = [r for r in results if r['status'] == 'Online']
    
    # Save to CSV
    with open('network_scan.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['ip', 'status', 'hostname'])
        writer.writeheader()
        writer.writerows(online_hosts)
    
    print(f"✓ Found {len(online_hosts)} online hosts")
    print("✓ Results saved to network_scan.csv")

if __name__ == "__main__":
    scan_network()