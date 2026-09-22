import subprocess
import platform
import tkinter as tk
from tkinter import scrolledtext

def get_system_info():
    """Get Windows system and network information."""
    
    info = []
    info.append(f"PC Name: {platform.node()}")
    info.append(f"OS: {platform.system()} {platform.release()}")
    info.append(f"Version: {platform.version()}")
    info.append(f"Machine: {platform.machine()}")
    info.append(f"Processor: {platform.processor()}")
    
    # Get network adapter info
    try:
        result = subprocess.run('ipconfig /all', shell=True, capture_output=True, text=True)
        info.append("\nNetwork Adapters:")
        info.append(result.stdout)
    except Exception as e:
        info.append(f"Error getting network info: {e}")
    
    return "\n".join(info)

def show_system_info():
    """Get system info and display in text area."""
    info = get_system_info()
    text_output.delete(1.0, tk.END)
    text_output.insert(1.0, info)

# Create GUI
root = tk.Tk()
root.title("System Information")
root.geometry("800x600")

# Button
btn_get_info = tk.Button(root, text="Get System Info", command=show_system_info)
btn_get_info.pack(pady=10)

# Output text area
text_output = scrolledtext.ScrolledText(root, width=100, height=35)
text_output.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root.mainloop()