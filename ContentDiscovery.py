import os
import subprocess
import json
from datetime import datetime

def run_command(command, output_file):
    with open(output_file, "w") as f:
        process = subprocess.run(command, shell=True, stdout=f, stderr=subprocess.DEVNULL)
    #print(f"Results saved to {output_file}")

def katana_scan(target, output_dir):
    output_file = f"{output_dir}/katana.txt"
    command = f"katana -u {target} -o {output_file}"
    run_command(command, output_file)

def gobuster_scan(target, output_dir):
    output_file = f"{output_dir}/gobuster.txt"
    command = f"gobuster dir -u {target} -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -o {output_file}"
    run_command(command, output_file)

def feroxbuster_scan(target, output_dir):
    output_file = f"{output_dir}/feroxbuster.txt"
    command = f"feroxbuster -u {target} -o {output_file}"
    run_command(command, output_file)

def gospider_scan(target, output_dir):
    output_file = f"{output_dir}/gospider.txt"
    command = f"gospider -s {target} -o {output_file}"
    run_command(command, output_file)

def dirsearch_scan(target, output_dir):
    output_file = f"{output_dir}/dirsearch.txt"
    command = f"dirsearch -u {target} -e php,html,js -o {output_file}"
    run_command(command, output_file)

def parse_results(output_dir):
    results = {}
    for tool in ["katana", "gobuster", "feroxbuster", "gospider", "dirsearch"]:
        file_path = f"{output_dir}/{tool}.txt"
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                results[tool] = [line.strip() for line in f.readlines() if line.strip()]

    filtered_results = {tool: list(set(data)) for tool, data in results.items() if data}
    with open(f"{output_dir}/parsed_results.json", "w") as f:
        json.dump(filtered_results, f, indent=4)
    print("Parsed results saved to parsed_results.json")

def main():
    target = input("Enter target domain: ")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"results_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)

    katana_scan(target, output_dir)
    gobuster_scan(target, output_dir)
    feroxbuster_scan(target, output_dir)
    gospider_scan(target, output_dir)
    dirsearch_scan(target, output_dir)

    parse_results(output_dir)
    print("Scanning completed. Check the results folder.")

if __name__ == "__main__":
    main()
