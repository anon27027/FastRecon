import subprocess
import re
import argparse
import concurrent.futures
import socket
import time
import csv
from datetime import datetime

result = {}

def run_nmap_scan(ip_address):
    result = subprocess.run(
        ['PortScanner/Script/host.sh', ip_address],  
        capture_output=True,  
        text=True  
    )
    
    return result.stdout, result.stderr

def run_nmap_port(ip_list_file):
    result = subprocess.run(['PortScanner/Script/ports.sh', ip_list_file], capture_output=True, text=True)

    return result.stdout

def run_naabu_port(ipaddress):
    # Run the naabu scan with the corrected script and output handling
    result = subprocess.run(['PortScanner/Script/fastPorts.sh', ipaddress], capture_output=True, text=True)
    return result.stdout

def extract_ports(nmap_output):
    ports_services = {}
    pattern = re.compile(r'(\d{1,5})/tcp\s+(\w+)\s+(\w+)')
    for match in pattern.findall(nmap_output):
        port, state, service = match
        ports_services[int(port)] = service
    return ports_services

def extract_host_ip(nmap_output):
    matches = set(re.findall(r'\(([\d.]+)\)', nmap_output))
    return matches, len(matches)

def process_naabu(host):
    result[host]=dict()
    def extract_port(val):
        match = re.search(r'\d+\.\d+\.\d+\.\d+:(\d+)', val)
        if match: 
            port = match.group(1) 
            service_name =socket.getservbyport(int(port))
            result[host][port]=service_name
            print(f'|{host}\t|\t {port}({service_name})')
            
    stdout = run_naabu_port(host).split('\n')
    if stdout:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            (executor.map(extract_port, stdout))
    if result[host]=={}:
        del result[host]
   

def process_nmap(host):
    result[host]=dict()
    stdout = run_nmap_port(host)
    open_ports = extract_ports(stdout)
    for op in open_ports:
        result[host][op]=open_ports[op]
        print(f'|{host}\t|\t {op}({open_ports[op]})')
    if result[host]=={}:
        del result[host]


def save_log(hosts):
    if result == {}:
        print("No Open Ports Found")
    
    else:
        def sanitize(value):        
            if isinstance(value, str):
                return ''.join(c if c.isprintable() else '' for c in value) 
            return value

        max_pairs = max(len(ports) for ports in result.values())
        
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        hostsUp_output_file = f"logs/{args.ip}/hosts_up_{current_time}.txt"
        openPorts_output_file = f"logs/{args.ip}/PortScanner_{current_time}.csv"

        with open(openPorts_output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            
            # Add header to CSV
            writer.writerow(["IP Address"] + ["Port", "Protocol"] * max_pairs)
            
            # Write data rows
            for ip, ports in result.items():
                row = [ip]  # Start with the IP address
                for port, protocol in ports.items():
                    row.extend([port, sanitize(protocol)])  # Add sanitized protocol
                writer.writerow(row)

        with open(hostsUp_output_file, "w") as file:
            for host in hosts:
                file.write(f"{host}\n")
        print(f"Logs saved to {hostsUp_output_file} and {openPorts_output_file}")    


parser = argparse.ArgumentParser(description='Scan IP Range and Scan Type Needed as Arguments')

parser.add_argument('ip', type=str, help='IP Range Missing')
parser.add_argument('Scan', type=str, help='Scan Type Missing')
args = parser.parse_args()
stdout, stderr = run_nmap_scan(args.ip)

if stdout:
    hosts, hosts_up = extract_host_ip(stdout)
    print(f"{hosts_up} host(s) up")
    start_time = time.time()

    if args.Scan == 'F':
        print(f'\rHOST \t\t\t PORT')
        print('------------------------------')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(process_naabu, hosts)
        print('------------------------------')

    
    elif args.Scan == 'S':
        print(f'\rHOST \t\t\t PORT')
        print('------------------------------')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(lambda host: process_nmap(host), hosts)
        print('------------------------------')

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f'Time taken for scan: {elapsed_time:.2f} seconds')
    save_log(hosts)


if stderr:
    print(stderr)
