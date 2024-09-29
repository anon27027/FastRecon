import subprocess
import os
import waymore
import gau_python
# Define the target domain
target_domain = "blackhatethicalhacking.com" #any domain

# Define file paths to store results
gau_output = f"{target_domain}_gau.txt"
waymore_output = f"{target_domain}_waymore.txt"
linkfinder_output = f"{target_domain}_linkfinder.txt"
js_files_output = f"{target_domain}_js_files.txt"

# Function to run a shell command and save output to a file
def run_command(command, output_file):
    print(f"Running command: {command}")
    with open(output_file, "w") as file:
        result = subprocess.run(command, shell=True, stdout=file, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print(f"Error executing {command}: {result.stderr.decode()}")
        else:
            print(f"Command executed successfully. Output saved to {output_file}")


# 2. Run Waymore
print(f"Running Waymore for {target_domain}...")
waymore_command = f"waymore -i {target_domain} -mode U -oU {waymore_output}"
run_command(waymore_command, waymore_output)

# Check if Waymore output is empty
if os.path.getsize(waymore_output) == 0:
    print("Waymore command did not produce any output.")
else:
    print("Waymore output saved successfully.")

#Gau&Linkifnder here



print(f"Reconnaissance completed for {target_domain}. Check the following files for results:")
print(f" - GAU output: {gau_output}")
print(f" - Waymore output: {waymore_output}")
print(f" - Combined URLs: {combined_urls}")
print(f" - JavaScript files: {js_files_output}")
print(f" - LinkFinder results: {linkfinder_output}")
