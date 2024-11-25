'''INSTALL
https://github.com/projectdiscovery/katana
https://github.com/OJ/gobuster
https://github.com/jaeles-project/gospider

'''
#Content Discovery
import subprocess
import os

def run_katana(target_url, output_file):
    """
    Run Katana for content discovery.
    """
    try:
        print("[*] Running Katana...")
        result = subprocess.run(
            ["katana", "-u", target_url, "-o", output_file],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("[+] Katana completed successfully.")
        else:
            print(f"[-] Katana error: {result.stderr}")
    except FileNotFoundError:
        print("[-] Katana not found. Ensure it's installed and in your PATH.")

def run_gobuster(target_url, wordlist, output_file):
    """
    Run GoBuster for directory brute-forcing.
    """
    try:
        print("[*] Running GoBuster...")
        result = subprocess.run(
            ["gobuster", "dir", "-u", target_url, "-w", wordlist, "-o", output_file],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("[+] GoBuster completed successfully.")
        else:
            print(f"[-] GoBuster error: {result.stderr}")
    except FileNotFoundError:
        print("[-] GoBuster not found. Ensure it's installed and in your PATH.")

def run_gospider(target_url, output_file):
    """
    Run GoSpider for web crawling.
    """
    try:
        print("[*] Running GoSpider...")
        result = subprocess.run(
            ["gospider", "-s", target_url, "-o", output_file],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("[+] GoSpider completed successfully.")
        else:
            print(f"[-] GoSpider error: {result.stderr}")
    except FileNotFoundError:
        print("[-] GoSpider not found. Ensure it's installed and in your PATH.")

def main():
    # User input for the target website
    target_url = "blackhatethicalhacking.com"
    # Output directory for results
    output_dir = "content_discovery_results"
    os.makedirs(output_dir, exist_ok=True)

    # Wordlist for GoBuster
    wordlist = "static/endpoinst.txt"  # Replace with the path to your wordlist file

    # File paths for tool outputs
    katana_output = os.path.join(output_dir, "katana_output.txt")
    gobuster_output = os.path.join(output_dir, "gobuster_output.txt")
    gospider_output = os.path.join(output_dir, "gospider_output.txt")

    # Run the tools
    run_katana(target_url, katana_output)
    run_gobuster(target_url, wordlist, gobuster_output)
    run_gospider(target_url, gospider_output)

    print("\n[+] Content discovery completed. Results saved in the following files:")
    print(f"    Katana: {katana_output}")
    print(f"    GoBuster: {gobuster_output}")
    print(f"    GoSpider: {gospider_output}")

if __name__ == "__main__":
    main()
