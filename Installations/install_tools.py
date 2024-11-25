import os
import subprocess


# Set the directory for installations as the script's directory
INSTALL_DIR = os.path.dirname(os.path.abspath(__file__))

def run_command(command):
    """Run a shell command and print output."""
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running command: {command}\n{e}")
        exit(1)

def install_apt_dependencies():
    """Install system dependencies using apt."""
    print("Installing system dependencies...")
    run_command("sudo apt update")
    run_command("sudo apt install -y git python3-pip golang nmap")  # Added nmap installation

def install_sublist3r():
    """Install Sublist3r."""
    print("Installing Sublist3r...")

    sublist3r_dir = f'{INSTALL_DIR}/Sublist3r'

    if os.path.isdir(sublist3r_dir):
        print(f"[*] Sublist3r is already installed at {sublist3r_dir}.")
    else:
        run_command(f"git clone https://github.com/aboul3la/Sublist3r.git {INSTALL_DIR}/Sublist3r")
        run_command(f"cd {INSTALL_DIR}/Sublist3r && sudo pip3 install -r requirements.txt")

def install_amass():
    """Install Amass."""
    print("Installing Amass...")
    run_command("sudo apt install amass")

def install_findomain():
    """Install Findomain."""
    print("Installing Findomain...")
    findomain_dir = os.path.join(INSTALL_DIR, "findomain")

    if os.path.isdir(findomain_dir):
        print(f"[*] FindDomain is already installed at {findomain_dir}.")
    else:
        os.makedirs(findomain_dir, exist_ok=True)
        run_command(f"wget https://github.com/Findomain/Findomain/releases/latest/download/findomain-linux.zip -P {findomain_dir}")
        run_command(f"unzip {findomain_dir}/findomain-linux.zip -d {findomain_dir}")
        run_command(f"sudo mv {findomain_dir}/findomain /usr/local/bin/")
        run_command("sudo chmod +x /usr/local/bin/findomain")
        print("[+] Findomain installed successfully.")


def install_subfinder():
    """Install Subfinder."""
    print("Installing Subfinder...")
    run_command("sudo apt install subfinder")

def install_chaos_client():
    """Install Chaos Client."""
    print("Installing Chaos Client...")
    run_command("go install -v github.com/projectdiscovery/chaos-client/cmd/chaos@latest")

def install_bbot():
    """Install BBOT."""
    print("Installing BBOT...")
    run_command("pip3 install bbot")

def install_massdns():
    """Install MassDNS for DNS brute-forcing."""
    print("Installing MassDNS (DNS brute-forcing tool)...")

    massdns_dir = os.path.join(INSTALL_DIR, "findomain")

    if os.path.isdir(massdns_dir):
        print(f"[*] MassDns is already installed at {massdns_dir}.")
    else:
        run_command(f"git clone https://github.com/blechschmidt/massdns.git {INSTALL_DIR}/massdns")
        run_command(f"cd {INSTALL_DIR}/massdns && make && sudo cp bin/massdns /usr/local/bin/")

def install_linkfinder():
    """Install LinkFinder."""
    print("Installing LinkFinder...")
    if not os.path.exists(f"{INSTALL_DIR}/linkfinder"):
        run_command(f"git clone https://github.com/GerbenJavado/LinkFinder {INSTALL_DIR}/linkfinder")
        run_command(f"cd {INSTALL_DIR}/linkfinder && python3 setup.py install")
        print("[+] LinkFinder installed successfully.")
    else:
        print("[*] LinkFinder is already installed.")

def install_nmap():
    """Install Nmap."""
    print("Installing Nmap...")
    run_command("sudo apt install -y nmap")
    print("[+] Nmap installed successfully.")

def install_naabu():
    """Install Naabu."""
    print("Installing Naabu...")
    run_command("sudo apt install -y naabu")
    
    

def main():
    """Main function to orchestrate the installations."""
    install_apt_dependencies()

    # Install individual tools
    install_sublist3r()
    install_amass()
    install_findomain()
    install_subfinder()
    install_chaos_client()
    install_bbot()
    install_massdns()
    install_linkfinder()
    install_nmap()  # Added Nmap installation
    install_naabu()  # Added Naabu installation

    print("All tools installed successfully.")

if __name__ == "__main__":
    main()
