import subprocess
import re
import argparse
import concurrent.futures
import socket
import time

def run_nmap_scan(ip_address):
    result = subprocess.run(
        ['Script/host.sh', ip_address],  
        capture_output=True,  
        text=True  
    )
    
    return result.stdout, result.stderr

def run_nmap_port(ip_list_file):
    result = subprocess.run(['Script/ports.sh', ip_list_file], capture_output=True, text=True)

    return result.stdout

def run_naabu_port(ipaddress):
    result = subprocess.run(['Script/fastPorts.sh', ipaddress], capture_output=True, text=True)

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
    def extract_port(val):
        match = re.search(r'\d+\.\d+\.\d+\.\d+:(\d+)', val)
        if match: 
            port = match.group(1) 
            service_name =socket.getservbyport(int(port))
            print(f'|{host}\t|\t {port}({service_name})')
            
    stdout = run_naabu_port(host).split('\n')
    if stdout:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            (executor.map(extract_port, stdout))
   

def process_nmap(host):
    stdout = run_nmap_port(host)
    open_ports = extract_ports(stdout)
    for op in open_ports:
        print(f'|{host}\t|\t {op}({open_ports[op]})')


parser = argparse.ArgumentParser(description='Scan Type')

parser.add_argument('ip', type=str, help='IP')
parser.add_argument('Scan', type=str, help='Scan Type')

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


if stderr:
    print(stderr)
