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

def check_ip_reputation(ip_address, api_key):
    """
    Check the reputation of the given IP address using AbuseIPDB API.

    :param ip_address: The IP address to check.
    :param api_key: Your AbuseIPDB API key.
    :return: A dictionary containing the API response or an error message.
    """
    url = f"https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Key": api_key,
        "Accept": "application/json"
    }
    params = {
        "ipAddress": ip_address,
        "maxAgeInDays": 90  # Optionally filter results from the last 90 days
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def main():
    # Ask the user for a website URL
    website = input("Enter a website URL (e.g., example.com): ").strip()

    # Provide your AbuseIPDB API key
    api_key = "7212f012c685a2804af2a272ed1a575d46f676b82fa3924df498e6af09c69919c5379448af4c2010"  # Replace with your actual API key

    # Resolve the domain to an IP address
    ip_result = get_ip_from_domain(website)

    if isinstance(ip_result, dict) and "error" in ip_result:
        print(f"Error resolving domain: {ip_result['error']}")
        return

    print(f"Resolved IP address for {website}: {ip_result}")

    # Check the IP reputation
    reputation_result = check_ip_reputation(ip_result, api_key)

    # Display the results
    if "error" in reputation_result:
        print(f"Error fetching IP reputation: {reputation_result['error']}")
    else:
        print("\nAbuseIPDB Reputation Data:")
        for key, value in reputation_result["data"].items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()
