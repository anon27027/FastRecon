import subprocess
import os
import argparse
import socket
import sys

# Function to run Eyewitness from an external Python script
def run_eyewitness(domain):
    try:
        # Path to the EyeWitness.py script inside the 'Python' folder
        eyewitness_path = "Installations/EyeWitness/Python/EyeWitness.py"  # Update this path

        # Command to run Eyewitness with the given domain
        command = ['python3', eyewitness_path, '--url', domain, '--web']

        # Run the command
        subprocess.run(command, check=True)
        return {"message": f"Eyewitness screenshot captured for {domain}."}
    except subprocess.CalledProcessError as e:
        return {"error": f"Error capturing screenshot with Eyewitness: {str(e)}"}

# Function to run GoWitness for capturing screenshots
def run_gowitness(domain):
    try:
        # Path to the GoWitness binary
        gowitness_path = "gowitness"  # Update this path

        # Command to run GoWitness with the given domain
        command = [gowitness_path, 'capture', '--url', domain, '--no-retry']

        # Run the command
        subprocess.run(command, check=True)
        return {"message": f"GoWitness screenshot captured for {domain}."}
    except subprocess.CalledProcessError as e:
        return {"error": f"Error capturing screenshot with GoWitness: {str(e)}"}

# Function to get IP from domain
def get_ip_from_domain(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror as e:
        return {"error": str(e)}

# Function to save logs to a file
def save_log(domain, log_data):
    # Define log file path
    log_directory = f"logs/{domain}"
    os.makedirs(log_directory, exist_ok=True)  # Create directory if it doesn't exist
    log_file = f"{log_directory}/screenshotting.txt"

    with open(log_file, 'w') as file:
        file.write(log_data)
    print(log_data)
    print(f"[+] Log saved to {log_file}")

# Main function
def main():
    parser = argparse.ArgumentParser(description="Screenshotting (Eyewitness & GoWitness).")
    parser.add_argument("-t", "--target", help="Domain to capture a screenshot", required=True)
    parser.add_argument("-m", "--method", choices=["eyewitness", "gowitness"], default="eyewitness", help="Choose screenshotting method")
    args = parser.parse_args()

    target = args.target
    method = args.method
    log_data = f"\nPerforming screenshot capture for: {target}\n"

    # Select method for screenshotting
    if method == "eyewitness":
        log_data += "[+] Running Eyewitness for screenshot capture...\n"
        result = run_eyewitness(target)
    else:
        log_data += "[+] Running GoWitness for screenshot capture...\n"
        result = run_gowitness(target)
    
    if "error" in result:
        log_data += f"Error: {result['error']}\n"
    else:
        log_data += f"{result['message']}\n"

    # Save log data to file
    save_log(target, log_data)

if __name__ == "__main__":
    main()
