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

# 1. Run GAU (Get All URLs)*
print(f"Running GAU for {target_domain}...")
gau_command = f"gau {target_domain}"
run_command(gau_command, gau_output)

# Check if GAU output is empty
if os.path.getsize(gau_output) == 0:
    print("GAU command did not produce any output.")
else:
    print("GAU output saved successfully.")

# 2. Run Waymore
print(f"Running Waymore for {target_domain}...")
waymore_command = f"waymore -i {target_domain} -mode U -oU {waymore_output}"
run_command(waymore_command, waymore_output)

# Check if Waymore output is empty
if os.path.getsize(waymore_output) == 0:
    print("Waymore command did not produce any output.")
else:
    print("Waymore output saved successfully.")

# Combine URLs from gau and waymore
combined_urls = f"{target_domain}_combined_urls.txt"
with open(combined_urls, "w") as outfile:
    for fname in [gau_output, waymore_output]:
        with open(fname) as infile:
            outfile.write(infile.read())

# Check if Combined URLs file is empty
if os.path.getsize(combined_urls) == 0:
    print("No combined URLs found.")
else:
    print("Combined URLs file created successfully.")

# 3. Extract JavaScript files from combined URLs
print("Extracting JavaScript files...")
js_files_command = f"grep -E '\\.js($|\\?)' {combined_urls} | sort -u"
run_command(js_files_command, js_files_output)

# Check if JavaScript files output is empty
if os.path.getsize(js_files_output) == 0:
    print("No JavaScript files found.")
else:
    print("JavaScript files extracted successfully.")

# 4. Run LinkFinder on each JavaScript file*
print("Running LinkFinder on JavaScript files...")
with open(js_files_output, "r") as js_files:
    for js_file in js_files:
        js_file = js_file.strip()
        linkfinder_command = f"linkfinder -i {js_file} -o cli "
        print(f"Processing {js_file}...")
        run_command(linkfinder_command, linkfinder_output)



print(f"Reconnaissance completed for {target_domain}. Check the following files for results:")
print(f" - GAU output: {gau_output}")
print(f" - Waymore output: {waymore_output}")
print(f" - Combined URLs: {combined_urls}")
print(f" - JavaScript files: {js_files_output}")
print(f" - LinkFinder results: {linkfinder_output}")
