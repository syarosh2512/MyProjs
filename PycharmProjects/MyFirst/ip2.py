import requests
from requests.exceptions import RequestException


def get_public_ip():
    url = 'https://api.ipify.org?format=json'
    try:
        # Adding verify=False to bypass SSL verification - Note: this reduces security!
        response = requests.get(url, timeout=5, verify=False)
        # Suppress urllib3 warnings about unverified HTTPS requests
        requests.packages.urllib3.disable_warnings()

        response.raise_for_status()
        ip_data = response.json()

        if 'ip' not in ip_data:
            raise ValueError("Unexpected API response format")

        return ip_data['ip']

    except RequestException as e:
        raise ConnectionError(f"Failed to fetch IP address: {str(e)}")
    except (ValueError, KeyError) as e:
        raise ValueError(f"Failed to parse IP data: {str(e)}")


if __name__ == "__main__":
    try:
        public_ip = get_public_ip()
        print(f"Public IP Address: {public_ip}")
    except Exception as e:
        print(f"Error: {str(e)}")
