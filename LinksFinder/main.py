import subprocess
import os
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description="Reconnaissance script to extract URLs and find JavaScript files.")
parser.add_argument("target_domain", help="Target domain to extract URLs from.")
parser.add_argument("action", choices=["S", "F"], help="Action to perform: 'S' for Waymore or 'F' for GAU.")

# Parse arguments
args = parser.parse_args()

# Define file paths to store results
gau_output = f"logs/{args.target_domain}/urls.txt"
waymore_output = f"logs/{args.target_domain}/hist_data.txt"
js_files_output = f"logs/{args.target_domain}/js_files.txt"
linkfinder_output = f"logs/{args.target_domain}/linkfinder.txt"

# Ensure the target domain directory exists
os.makedirs(os.path.dirname(gau_output), exist_ok=True)

with open(gau_output, 'w') as file:
    file.write("")  # Optionally, you can leave this empty or add a header text
print(f"File {gau_output} created.")

def run_command(command, output_file):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print(result)
    
    if result.stdout:
        # Save the output to the file if there's any content
        with open(output_file, "w+") as file:
            file.write(result.stdout.decode())
        print(f"Command executed successfully. Output saved to {output_file}")
    else:
        print(f"Command did not produce any output: {command}")
        
    # Check for errors in stderr
    if result.returncode != 0:
        print(f"Error executing {command}: {result.stderr.decode()}")

# 1. Run GAU (Get All URLs) or Waymore based on the user's input
if args.action == 'S':
    print(f"Running Waymore for historical data of {args.target_domain}...")
    waymore_command = f"waymore -i {args.target_domain} -mode U -oU {waymore_output}"
    run_command(waymore_command, waymore_output)

    # Check if Waymore output is empty
    if os.path.getsize(waymore_output) == 0:
        print("Command did not produce any output.")
    else:
        print("Historical data saved successfully.")

elif args.action == 'F':
    print(f"Extracting all URL(s) from {args.target_domain}")
    gau_command = f"gau {args.target_domain}"
    run_command(gau_command, gau_output)

    # Check if GAU output is empty
    if os.path.getsize(gau_output) == 0:
        print("Command did not produce any output.")
    else:
        print("URL(s) saved successfully.")

# 2. Extract JavaScript files from the output
print("Extracting JavaScript files...")
if args.action == 'S' and os.path.getsize(waymore_output) > 0:
    js_files_command = f"grep -E '\\.js($|\\?)' {waymore_output} | sort -u"
elif args.action == 'F' and os.path.getsize(gau_output) > 0:
    js_files_command = f"grep -E '\\.js($|\\?)' {gau_output} | sort -u"
else:
    print("No URLs found to extract JavaScript files.")
    exit()

run_command(js_files_command, js_files_output)

# Check if JavaScript files output is empty
if os.path.getsize(js_files_output) == 0:
    print("No JavaScript files found.")
else:
    print("JavaScript files extracted successfully.")

# 3. Run LinkFinder on each JavaScript file
print("Running LinkFinder on JavaScript files...")
with open(js_files_output, "r") as js_files:
    for js_file in js_files:
        js_file = js_file.strip()
        linkfinder_command = f"linkfinder -i {js_file} -o cli"
        run_command(linkfinder_command, linkfinder_output)

if args.action == 'S':
    print(f" - Waymore output: {waymore_output}")
elif args.action == 'F':
    print(f" - GAU output: {gau_output}")
print(f" - JavaScript files: {js_files_output}")
print(f" - LinkFinder results: {linkfinder_output}")
