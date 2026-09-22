import subprocess
import time

def check_shares():
    """Check network shares with proper timeout handling."""
    
    ip = "10.221.131.151"
    
    try:
        # Use shorter timeout and handle error
        result = subprocess.run(
            ["net", "view", f"\\\\{ip}"], 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        
        if result.returncode == 0:
            print(f"✓ Shares found on {ip}:")
            print(result.stdout)
        else:
            print(f"⚠ No shares accessible on {ip}")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print(f"⚠ Connection to {ip} timed out")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_shares()