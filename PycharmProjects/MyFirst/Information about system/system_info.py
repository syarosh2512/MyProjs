import subprocess
import platform
import socket

def get_system_info():
    """Get Windows system and network information and save to file."""
    
    info = []
    
    # Basic system info
    info.append(f"OS: {platform.system()} {platform.release()}")
    info.append(f"Version: {platform.version()}")
    info.append(f"Machine: {platform.machine()}")
    info.append(f"Processor: {platform.processor()}")
    info.append(f"Computer Name: {socket.gethostname()}")
    
    # Get IP configuration
    try:
        result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            info.append("\n=== Network Configuration ===")
            info.append(result.stdout)
        else:
            info.append("\nError: Could not get network configuration")
    except Exception as e:
        info.append(f"\nNetwork info error: {e}")
    
    # Save to file
    try:
        with open('system_info.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(info))
        print("✓ System info saved to system_info.txt")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    get_system_info()