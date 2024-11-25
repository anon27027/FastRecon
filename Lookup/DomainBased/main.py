import requests
import whois  # Ensure this is the correct version of the whois library
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

# Function to perform WHOIS lookup
def whois_lookup(domain):
    try:
        w = whois.whois(domain)
        return w
    except Exception as e:
        return {"error": str(e)}

# Function to get archived versions from the Wayback Machine
def wayback_lookup(domain):
    url = f"http://archive.org/wayback/available?url={domain}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'archived_snapshots' in data and 'closest' in data['archived_snapshots']:
            return data['archived_snapshots']['closest']
        else:
            return {"message": "No archived version found."}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Function to check if an AWS S3 bucket is publicly accessible
def check_aws_bucket(bucket_name):
    url = f"http://{bucket_name}.s3.amazonaws.com"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return {"message": "Bucket is publicly accessible."}
        else:
            return {"message": "Bucket is not publicly accessible."}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Function to save logs to a file
def save_log(domain, log_data):
    # Define log file path
    log_directory = f"logs/{domain}"
    os.makedirs(log_directory, exist_ok=True)  # Create directory if it doesn't exist
    log_file = f"{log_directory}/domainlookup.txt"

    with open(log_file, 'w') as file:
        file.write(log_data)
    print(log_data)
    print(f"[+] Log saved to {log_file}")

# Main function
def main():
    parser = argparse.ArgumentParser(description="Domain-based Tech Lookup.")
    parser.add_argument("-t", "--target", help="Domain to look up WHOIS, Wayback, and AWS Bucket status", required=True)
    args = parser.parse_args()

    target = args.target
    log_data = f"\nPerforming domain-based lookups for: {target}\n"

    # WHOIS lookup
    log_data += "[+] WHOIS Information:\n"
    whois_info = whois_lookup(target)
    if "error" in whois_info:
        log_data += f"Error: {whois_info['error']}\n"
    else:
        log_data += f"{whois_info}\n"

    # Wayback Machine lookup
    log_data += "\n[+] Wayback Machine Archived Versions:\n"
    wayback_info = wayback_lookup(target)
    if "error" in wayback_info:
        log_data += f"Error: {wayback_info['error']}\n"
    else:
        log_data += f"Closest archived version: {wayback_info.get('url', 'No archived version found')}\n"

    # AWS S3 bucket check (if domain resolves to an IP)
    log_data += "\n[+] AWS S3 Bucket Status:\n"
    ip_address = get_ip_from_domain(target)
    if "error" in ip_address:
        log_data += f"Error: {ip_address['error']}\n"
    else:
        bucket_check = check_aws_bucket(target)
        log_data += f"{bucket_check.get('message', 'Error checking AWS bucket.')}\n"

    # Save log data to file
    save_log(target, log_data)

if __name__ == "__main__":
    main()
