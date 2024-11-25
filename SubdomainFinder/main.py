import argparse
import subprocess
import time
import os
import socket
import threading
import tempfile

def run_command(command, retries=2):
    """Run a shell command, retrying up to `retries` times if it fails."""
    for attempt in range(retries + 1):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError:
            if attempt == retries:
                return None
            time.sleep(2)  # Wait before retrying

def get_ip_domain(ip):
    """Resolve an IP address to a domain name using reverse DNS lookup."""
    try:
        domain = socket.gethostbyaddr(str(ip))
        return domain[0]
    except socket.herror:
        return None

def run_subdomain_tool(command, output_file):
    """Run a subdomain discovery tool."""
    output = run_command(command)
    if output is not None and os.path.exists(output_file):
        with open(output_file, 'r') as file:
            return file.read().splitlines()
    return []

def get_subdomains(domain):
    """Get subdomains using various tools."""
    subdomains = set()
    temp_dir = tempfile.mkdtemp()

    tools = [
        ('amass enum -passive -d', os.path.join(temp_dir, 'amass_output.txt')),
        ('findomain -t', os.path.join(temp_dir, 'findomain_output.txt')),
        ('subfinder -d', os.path.join(temp_dir, 'subfinder_output.txt')),
        ('chaos -d', os.path.join(temp_dir, 'chaos_output.txt')),
        ('bbot ', os.path.join(temp_dir, 'bbot_output.txt'))
    ]

    for command, output_file in tools:
        subdomains.update(run_subdomain_tool(f'{command} {domain} -o {output_file}', output_file))

    # Clean up temporary directory after use
    if os.path.exists(temp_dir):
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)

    return subdomains

def save_subdomains_to_file(domain, subdomains):
    """Create directory structure and save subdomains to a file."""
    log_dir = "logs"
    domain_dir = os.path.join(log_dir, domain)

    # Create the logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create the domain directory if it doesn't exist
    if not os.path.exists(domain_dir):
        os.makedirs(domain_dir)

    # Save the subdomains to a file
    subdomain_file = os.path.join(domain_dir, "subdomain.txt")
    with open(subdomain_file, 'w') as file:
        for subdomain in sorted(subdomains):
            file.write(f"{subdomain}\n")

def find_subdomains_for_domain(domain):
    """Find subdomains for a given domain."""
    subdomains = get_subdomains(domain)
    if subdomains:
        print(f"[+] Found {len(subdomains)} unique subdomains for {domain}:")
        for subdomain in sorted(subdomains):
            print(subdomain)
        save_subdomains_to_file(domain, subdomains)  # Save the subdomains to file
    else:
        print(f"[-] No subdomains found for {domain}.")

def is_valid_ip(address):
    """Check if the provided address is a valid IP."""
    try:
        socket.inet_aton(address)
        return True
    except socket.error:
        return False

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Find subdomains for a domain or IP.")
    parser.add_argument("-t", "--target", help="Domain or IP address to find subdomains for", required=True)
    args = parser.parse_args()

    target = args.target

    # If the target is an IP address, resolve it to a domain
    if is_valid_ip(target):
        domain = get_ip_domain(target)
        if domain:
            print(f"[+] Resolved IP {target} to domain: {domain}")
        else:
            print(f"[-] Could not resolve IP {target} to a domain.")
            return
    else:
        domain = target

    find_subdomains_for_domain(domain)

if __name__ == '__main__':
    main()