from netmiko import ConnectHandler
import os

# Define device types and commands as constants
HP_TYPES = {
    'comware': ('hp_comware', 'display current-configuration'),
    'procurve': ('hp_procurve', 'show running-config')
}

def download_hp_config(host, username, password, port=22, hp_type='comware', output_dir='.'):
    """Download configuration from HP network device."""
    # Get device type and command based on HP platform
    device_type, config_command = HP_TYPES.get(hp_type.lower(), HP_TYPES['comware'])
    
    # Create connection parameters
    device = {
        'device_type': device_type,
        'host': host,
        'username': username,
        'password': password,
        'port': port,
    }
    
    try:
        with ConnectHandler(**device) as conn:
            config = conn.send_command(config_command)
            
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Save to file with full path
            filename = os.path.join(output_dir, f"{host}_hp_config.txt")
            with open(filename, 'w') as f:
                f.write(config)
            
            print(f"Configuration saved to {filename}")
            return filename
            
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # Example usage with credentials removed
    download_hp_config(
        host='10.222.1.56',
        username='admin',
        password='<D62S0071501>',  # Replace with actual password
        hp_type='comware'
    )