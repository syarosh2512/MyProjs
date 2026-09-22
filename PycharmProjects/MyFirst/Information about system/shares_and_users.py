import subprocess

def show_shares_and_users():
    """Show all network shares and connected users on Windows PC and save to file."""
    
    with open('shares_and_users.txt', 'w') as f:
        f.write("=== Network Shares ===\n")
        try:
            result = subprocess.run('net share', shell=True, capture_output=True, text=True)
            f.write(result.stdout)
        except Exception as e:
            f.write(f"Error getting shares: {e}\n")
        
        f.write("\n=== Connected Users/Sessions ===\n")
        try:
            result = subprocess.run('net session', shell=True, capture_output=True, text=True)
            f.write(result.stdout)
        except Exception as e:
            f.write(f"Error getting sessions: {e}\n")
        
        f.write("\n=== Open Files ===\n")
        try:
            result = subprocess.run('net file', shell=True, capture_output=True, text=True)
            f.write(result.stdout)
        except Exception as e:
            f.write(f"Error getting open files: {e}\n")
        
        f.write("\n=== Current User Sessions ===\n")
        try:
            result = subprocess.run('query user', shell=True, capture_output=True, text=True)
            f.write(result.stdout)
        except Exception as e:
            f.write(f"Error getting user sessions: {e}\n")
    
    print("Shares and users information saved to shares_and_users.txt")

if __name__ == "__main__":
    show_shares_and_users()