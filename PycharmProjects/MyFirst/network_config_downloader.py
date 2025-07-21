from netmiko import ConnectHandler

def download_hp_config(host, username, password, port=22, hp_type='comware'):
    """
    Download configuration from HP network device using Netmiko
    hp_type: 'comware' for HP Comware/H3C or 'procurve' for HP ProCurve
    """
    # Set the correct device type based on HP platform
    if hp_type.lower() == 'comware':
        device_type = 'hp_comware'
        config_command = 'display current-configuration'
    else:  # ProCurve
        device_type = 'hp_procurve'
        config_command = 'show running-config'
    
    # Device connection parameters
    device = {
        'device_type': device_type,
        'host': host,
        'username': username,
        'password': password,
        'port': port,
    }
    
    try:
        # Connect to the device
        with ConnectHandler(**device) as conn:
            # Get the configuration
            config = conn.send_command(config_command)
            
            # Save to file
            filename = f"{host}_hp_config.txt"
            with open(filename, 'w') as f:
                f.write(config)
            
            print(f"HP configuration saved to {filename}")
            return filename
    
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # Example usage for HP device
    download_hp_config(
        host='10.222.1.49',
        username='admin',
        password='D62S0071501',
        hp_type='hp_procurve'  # Use 'comware' for HP Comware/H3C or 'procurve' for HP ProCurve
    )