import requests
import socket

def get_ip_from_domain(domain):
    """
    Resolve the domain name to an IP address.
    
    :param domain: The domain name to resolve.
    :return: The resolved IP address or an error message.
    """
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror as e:
        return {"error": str(e)}

def get_geolocation(ip_address, api_key):
    """
    Fetch geolocation data for the given IP address using IP2Location.io API.

    :param ip_address: The IP address to lookup.
    :param api_key: Your IP2Location.io API key.
    :return: A dictionary containing the geolocation data or an error message.
    """
    url = f"https://api.ip2location.io/?key={api_key}&ip={ip_address}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def main():
    # Ask the user for a website URL
    website = input("Enter a website URL (e.g., example.com): ").strip()

    # Provide your IP2Location.io API key
    api_key = "816FBDFE07BC95FAEC4490E15B64F80A"  # Replace with your actual API key

    # Resolve the domain to an IP address
    ip_result = get_ip_from_domain(website)

    if "error" in ip_result:
        print(f"Error resolving domain: {ip_result['error']}")
        return

    print(f"Resolved IP address for {website}: {ip_result}")

    # Get the geolocation data
    geolocation_result = get_geolocation(ip_result, api_key)

    # Display the results
    if "error" in geolocation_result:
        print(f"Error fetching geolocation: {geolocation_result['error']}")
    else:
        print("\nGeolocation Data:")
        for key, value in geolocation_result.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()
