import requests
import socket
import argparse
import os

# Function to get IP from domain
def get_ip_from_domain(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror as e:
        return {"error": str(e)}

# Function to get geolocation data
def get_geolocation(ip_address, api_key):
    url = f"https://api.ip2location.io/?key={api_key}&ip={ip_address}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Function to check if IP is valid
def is_valid_ip(address):
    try:
        socket.inet_aton(address)
        return True
    except socket.error:
        return False

# Function to save logs to a file
def save_log(domain, log_data):
    # Define log file path
    log_directory = f"logs/{domain}"
    os.makedirs(log_directory, exist_ok=True)  # Create directory if it doesn't exist
    log_file = f"{log_directory}/ipGeoLocation.txt"

    with open(log_file, 'w') as file:
        file.write(log_data)

    print(log_data)
    print(f"[+] Log saved to {log_file}")

# Main function
def main():
    api_key = "816FBDFE07BC95FAEC4490E15B64F80A"  

    parser = argparse.ArgumentParser(description="IP Location.")
    parser.add_argument("-t", "--target", help="Domain or IP address to find geolocation for", required=True)
    args = parser.parse_args()

    target = args.target
    log_data = f"\nPerforming IP geolocation lookup for: {target}\n"

    if is_valid_ip(target):
        ip = target
    else:
        ip = get_ip_from_domain(target)
        if ip:
            log_data += f"[+] Resolved Domain {target} to IP: {ip}\n"
        else:
            log_data += "[-] Could not resolve.\n"
            save_log(target, log_data)
            return

    # Get geolocation data
    geolocation_result = get_geolocation(ip, api_key)

    # Prepare log data for display and saving
    if "error" in geolocation_result:
        log_data += f"Error fetching geolocation: {geolocation_result['error']}\n"
    else:
        log_data += "\nGeolocation Data:\n"
        for key, value in geolocation_result.items():
            log_data += f"{key}: {value}\n"

    # Save log data to file
    save_log(target, log_data)

if __name__ == "__main__":
    main()
