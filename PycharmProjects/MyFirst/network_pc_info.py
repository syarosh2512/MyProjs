import subprocess
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import os
import getpass

def get_remote_pc_info(ip_address, username, password):
    """Get information about a remote PC in network with credentials."""
    
    info = []
    info.append(f"Script executed by: {getpass.getuser()}")
    info.append(f"Target PC: {ip_address}")
    info.append(f"Using credentials: {username} / {password}")
    info.append("=" * 50)
    
    # Use current user context if no specific credentials provided
    use_current_user = (password == "(current user)")
    
    # Ping test
    try:
        result = subprocess.run(f'ping -n 4 {ip_address}', shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            info.append("✓ PC is reachable")
        else:
            info.append("✗ PC is not reachable")
        info.append(f"\nPing Results:\n{result.stdout}")
    except Exception as e:
        info.append(f"Ping error: {e}")
    
    # Get system info via WMI
    try:
        if use_current_user:
            result = subprocess.run(f'wmic /node:"{ip_address}" computersystem get name,manufacturer,model', 
                                  shell=True, capture_output=True, text=True, timeout=15)
        else:
            result = subprocess.run(f'wmic /node:"{ip_address}" /user:"{username}" /password:"{password}" computersystem get name,manufacturer,model', 
                                  shell=True, capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            info.append(f"\nSystem Info:\n{result.stdout}")
        else:
            info.append(f"\nSystem Info Error: {result.stderr}")
    except Exception as e:
        info.append(f"\nSystem info error: {e}")
    
    # Get OS info via WMI
    try:
        if use_current_user:
            result = subprocess.run(f'wmic /node:"{ip_address}" os get caption,version', 
                                  shell=True, capture_output=True, text=True, timeout=15)
        else:
            result = subprocess.run(f'wmic /node:"{ip_address}" /user:"{username}" /password:"{password}" os get caption,version', 
                                  shell=True, capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            info.append(f"\nOS Info:\n{result.stdout}")
        else:
            info.append(f"\nOS Info Error: {result.stderr}")
    except Exception as e:
        info.append(f"\nOS info error: {e}")
    
    # Get network shares
    try:
        if use_current_user:
            result = subprocess.run(f'wmic /node:"{ip_address}" process call create "net share"', 
                                  shell=True, capture_output=True, text=True, timeout=10)
        else:
            result = subprocess.run(f'wmic /node:"{ip_address}" /user:"{username}" /password:"{password}" process call create "net share"', 
                                  shell=True, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            info.append(f"\nNetwork Shares:\n{result.stdout}")
        else:
            info.append(f"\nNetwork Shares Error: {result.stderr}")
    except Exception as e:
        info.append(f"\nShares error: {e}")
    
    return "\n".join(info)

def scan_pc():
    """Scan remote PC and display results."""
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    ip = entry_ip.get().strip()
    
    # Use current user if no username provided
    if not username:
        username = getpass.getuser()
        password = "(current user)"
    
    if not ip:
        messagebox.showerror("Error", "Please enter an IP address")
        return
    
    btn_scan.config(state='disabled', text='Scanning...')
    text_output.delete(1.0, tk.END)
    text_output.insert(1.0, f"Scanning {ip} with credentials...\n")
    
    def scan_thread():
        try:
            info = get_remote_pc_info(ip, username, password)
            text_output.delete(1.0, tk.END)
            text_output.insert(1.0, info)
        except Exception as e:
            text_output.delete(1.0, tk.END)
            text_output.insert(1.0, f"Error scanning {ip}: {e}")
        finally:
            btn_scan.config(state='normal', text='Scan PC')
    
    threading.Thread(target=scan_thread, daemon=True).start()

# Create GUI
root = tk.Tk()
root.title("Network PC Information Scanner")
root.geometry("900x700")

# Credentials frame
frame_creds = tk.Frame(root)
frame_creds.pack(pady=10)

tk.Label(frame_creds, text="Username (domain\\user or .\\user):").grid(row=0, column=0, padx=5)
entry_username = tk.Entry(frame_creds, width=25)
entry_username.grid(row=0, column=1, padx=5)

tk.Label(frame_creds, text="Password:").grid(row=0, column=2, padx=5)
entry_password = tk.Entry(frame_creds, width=20, show="*")
entry_password.grid(row=0, column=3, padx=5)

# IP input frame
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="IP Address:").pack(side=tk.LEFT)
entry_ip = tk.Entry(frame_input, width=20)
entry_ip.pack(side=tk.LEFT, padx=5)

btn_scan = tk.Button(frame_input, text="Scan PC", command=scan_pc)
btn_scan.pack(side=tk.LEFT, padx=5)

# Output text area
text_output = scrolledtext.ScrolledText(root, width=110, height=40)
text_output.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root.mainloop()