# Module for retrieving the public IP address using ipify.org API
import requests
import warnings
from requests.exceptions import RequestException
from urllib3.exceptions import InsecureRequestWarning


def get_public_ip(verify_ssl=True):
    """Fetch the public IP address of the current machine.
    
    Args:
        verify_ssl (bool): Whether to verify SSL certificates (default: True)
    
    Returns:
        str: The public IP address
        
    Raises:
        ConnectionError: If network request fails
        ValueError: If response parsing fails
    """
    # API endpoint for IP address retrieval
    url = 'https://api.ipify.org?format=json'
    
    # Suppress only InsecureRequestWarning when verify_ssl is False
    if not verify_ssl:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', InsecureRequestWarning)
            return _get_ip_from_url(url, verify_ssl)
    else:
        return _get_ip_from_url(url, verify_ssl)


def _get_ip_from_url(url, verify_ssl):
    """Helper function to make the actual request."""
    try:
        # Make request with timeout to prevent hanging
        # Set verify=False to bypass SSL certificate verification if needed
        response = requests.get(url, timeout=5, verify=verify_ssl)
        response.raise_for_status()  # Raise exception for HTTP errors
        ip_data = response.json()

        # Validate response format
        if 'ip' not in ip_data:
            raise ValueError("Unexpected API response format")

        return ip_data['ip']

    except RequestException as e:
        # Handle network-related errors
        raise ConnectionError(f"Failed to fetch IP address: {str(e)}")
    except (ValueError, KeyError) as e:
        # Handle parsing errors
        raise ValueError(f"Failed to parse IP data: {str(e)}")


if __name__ == "__main__":
    try:
        # First try with SSL verification
        try:
            public_ip = get_public_ip(verify_ssl=True)
        except ConnectionError:
            # If SSL verification fails, try without it
            print("SSL verification failed, trying without verification...")
            public_ip = get_public_ip(verify_ssl=False)
            print("Warning: SSL verification was disabled")
        
        print(f"Public IP Address: {public_ip}")
    except Exception as e:
        print(f"Error: {str(e)}")
