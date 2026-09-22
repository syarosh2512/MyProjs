import subprocess
import tempfile
import os

def connect_rdp(server, username, password):
    """Connect to Windows server via RDP using mstsc."""
    
    rdp_content = f"""full address:s:{server}
username:s:{username}
"""
    
    rdp_file = None
    try:
        # Create temporary RDP file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.rdp', delete=False) as f:
            f.write(rdp_content)
            rdp_file = f.name
        
        # Store credentials and launch RDP
        subprocess.run(f'cmdkey /generic:TERMSRV/{server} /user:{username} /pass:"{password}"', shell=True)
        subprocess.run(f'mstsc "{rdp_file}"', shell=True)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up
        if rdp_file and os.path.exists(rdp_file):
            os.unlink(rdp_file)
        subprocess.run(f'cmdkey /delete:TERMSRV/{server}', shell=True, capture_output=True)

if __name__ == "__main__":
    connect_rdp("10.221.131.14", "SRVS0071501", "MiaNetty@2512Danny")