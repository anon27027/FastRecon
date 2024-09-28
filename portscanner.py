import subprocess
import re
import csv
import argparse

def run_nmap_scan(ip_address):
    result = subprocess.run(
        ['Script/host.sh', ip_address],  
        capture_output=True,  
        text=True  
    )
    
    return result.stdout, result.stderr

def run_nmap_port(ip_list_file):
    result = subprocess.run(['Script/ports.sh', ip_list_file], capture_output=True, text=True)

    return result.stdout, result.stderr

def run_naabu_port(ipaddress):
    result = subprocess.run(['Script/fastPorts.sh', ipaddress], capture_output=True, text=True)

    return result.stdout, result.stderr

def extract_hosts_up(nmap_output):
    match = re.search(r'(\d+) hosts? up', nmap_output)
    if match:
        return match.group(1) 
    return "0"

def extract_host_ip(nmap_output):
    matches = set(re.findall(r'\(([\d.]+)\)', nmap_output))
    return matches

def extract_ports(nmap_output):
    ports_services = {}
    pattern = re.compile(r'(\d{1,5})/tcp\s+(\w+)\s+(\w+)')
    for match in pattern.findall(nmap_output):
        port, state, service = match
        ports_services[int(port)] = service
    return ports_services

parser = argparse.ArgumentParser(description='Scan Type')

parser.add_argument('ip', type=str, help='IP')
parser.add_argument('Scan', type=str, help='Scan Type')

args = parser.parse_args()
stdout, stderr = run_nmap_scan(args.ip)
print(args.ip)

if stdout:
    hosts = extract_host_ip(stdout)
    hosts_up = extract_hosts_up(stdout)
    print(hosts)
    print(f"{hosts_up} hosts up")

    ports = {}

    if args.Scan == 'F':
        for host in hosts:
            stdout, stderr = run_naabu_port(host)
            if stdout:
                print(stdout)
    elif args.Scan == 'S':
        for host in hosts:
            stdout, stderr = run_nmap_port(host)
            open_ports = extract_ports(stdout)
            ports[host]=open_ports
            print(open_ports)

if stderr:
    print(stderr)
