import subprocess
import time
import os

def run_command(command, retries=2):
    """Run a shell command, retrying up to `retries` times if it fails."""
    for attempt in range(retries + 1):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"[-] Error running command: {command}. Attempt {attempt + 1} of {retries + 1}")
            if attempt == retries:
                print(f"[-] Skipping command: {command}")
                return None
            time.sleep(2)  # Wait for 2 seconds before retrying

def sublist3r(domain):
    """Run Sublist3r to find subdomains."""
    print("[+] Running Sublist3r...")
    command = f'python3 Sublist3r/sublist3r.py -d {domain} -o sublist3r_output.txt'
    output = run_command(command)
    if output is not None and os.path.exists('sublist3r_output.txt'):
        with open('sublist3r_output.txt', 'r') as file:
            return file.read().splitlines()
    return []

def amass(domain):
    """Run Amass to find subdomains."""
    print("[+] Running Amass...")
    command = f'amass enum -passive -d {domain} -o amass_output.txt'
    output = run_command(command)
    if output is not None and os.path.exists('amass_output.txt'):
        with open('amass_output.txt', 'r') as file:
            return file.read().splitlines()
    return []

def findomain(domain):
    """Run Findomain to find subdomains."""
    print("[+] Running Findomain...")
    command = f'findomain -t {domain} -u findomain_output.txt'
    output = run_command(command)
    if output is not None and os.path.exists('findomain_output.txt'):
        with open('findomain_output.txt', 'r') as file:
            return file.read().splitlines()
    return []

def subfinder(domain):
    """Run Subfinder to find subdomains."""
    print("[+] Running Subfinder...")
    command = f'subfinder -d {domain} -o subfinder_output.txt'
    output = run_command(command)
    if output is not None and os.path.exists('subfinder_output.txt'):
        with open('subfinder_output.txt', 'r') as file:
            return file.read().splitlines()
    return []

def chaos(domain):
    """Run Chaos client to find subdomains."""
    print("[+] Running Chaos-client...")
    command = f'chaos -d {domain} -o chaos_output.txt'
    output = run_command(command)
    if output is not None and os.path.exists('chaos_output.txt'):
        with open('chaos_output.txt', 'r') as file:
            return file.read().splitlines()
    return []

def bbot(domain):
    """Run BBOT to find subdomains."""
    print("[+] Running BBOT...")
    command = f'bbot -q {domain} --output bbot_output.txt'
    output = run_command(command)
    if output is not None and os.path.exists('bbot_output.txt'):
        with open('bbot_output.txt', 'r') as file:
            return file.read().splitlines()
    return []

def get_subdomains(domain):
    """Get subdomains using all installed tools and consolidate the results."""
    subdomains = set()

    # Run tools and consolidate results
    subdomains.update(sublist3r(domain))
    subdomains.update(amass(domain))
    subdomains.update(findomain(domain))
    subdomains.update(subfinder(domain))
    subdomains.update(chaos(domain))
    subdomains.update(bbot(domain))

    return subdomains

def main():
    # Get domain from user input
    domain = input("Enter the domain name: ").strip()

    # Ensure the domain is valid
    if not domain:
        print("[-] Invalid domain.")
        return

    print(f"[+] Finding subdomains for: {domain}")
    
    # Get subdomains from all tools
    subdomains = get_subdomains(domain)

    # Output the result
    if subdomains:
        print(f"[+] Found {len(subdomains)} unique subdomains:")
        for subdomain in sorted(subdomains):
            print(subdomain)
    else:
        print("[-] No subdomains found.")

if __name__ == '__main__':
    main()
tme
