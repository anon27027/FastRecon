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

# Function to check IP reputation
def check_ip_reputation(ip_address, api_key):
    url = f"https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Key": api_key,
        "Accept": "application/json"
    }
    params = {
        "ipAddress": ip_address,
        "maxAgeInDays": 90  
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

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
    log_file = f"{log_directory}/abuseIP.txt"

    with open(log_file, 'w') as file:
        file.write(log_data)
    print(log_data)
    print(f"[+] Log saved to {log_file}")

# Main function
def main():
    api_key = "7212f012c685a2804af2a272ed1a575d46f676b82fa3924df498e6af09c69919c5379448af4c2010"  

    parser = argparse.ArgumentParser(description="Check IP Malicious Reputation.")
    parser.add_argument("-t", "--target", help="Domain or IP address to check for IP reputation", required=True)
    args = parser.parse_args()

    target = args.target
    log_data = f"\nPerforming IP reputation lookup for: {target}\n"

 
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

    # Get reputation data
    reputation_result = check_ip_reputation(ip, api_key)

    # Prepare the log data for the results
    if "error" in reputation_result:
        log_data += f"Error fetching IP reputation: {reputation_result['error']}\n"
    else:
        log_data += "\nAbuseIPDB Reputation Data:\n"
        for key, value in reputation_result["data"].items():
            log_data += f"{key}: {value}\n"

    # Save log data to file
    save_log(target, log_data)

if __name__ == "__main__":
    main()
