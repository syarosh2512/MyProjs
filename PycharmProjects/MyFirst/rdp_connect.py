import subprocess

def connect_rdp(server, username, password):
    """Connect to Windows server via RDP using mstsc."""
    
    try:
        # Store credentials and launch RDP
        subprocess.run(f'cmdkey /generic:TERMSRV/{server} /user:{username} /pass:"{password}"', shell=True)
        subprocess.run(f'mstsc /v:{server}', shell=True)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up credentials
        subprocess.run(f'cmdkey /delete:TERMSRV/{server}', shell=True, capture_output=True)

if __name__ == "__main__":
    connect_rdp("10.222.1.250", "Administrator", "<password>")