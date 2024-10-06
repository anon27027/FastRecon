import os
import subprocess

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
    run_command("sudo apt install -y git python3-pip golang")

def install_sublist3r():
    """Install Sublist3r."""
    print("Installing Sublist3r...")
    run_command("git clone https://github.com/aboul3la/Sublist3r.git")
    run_command("cd Sublist3r && sudo pip3 install -r requirements.txt")

def install_amass():
    """Install Amass."""
    print("Installing Amass...")
    run_command("go install -v github.com/owasp-amass/amass/v3/...@master")

def install_findomain():
    """Install Findomain."""
    print("Installing Findomain...")
    run_command("wget https://github.com/Findomain/Findomain/releases/latest/download/findomain-linux.zip")
    run_command("unzip findomain-linux.zip && sudo mv findomain /usr/local/bin/ && chmod +x /usr/local/bin/findomain")

def install_subfinder():
    """Install Subfinder."""
    print("Installing Subfinder...")
    run_command("go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest")

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
    run_command("git clone https://github.com/blechschmidt/massdns.git")
    run_command("cd massdns && make && sudo cp bin/massdns /usr/local/bin/")

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

    print("All tools installed successfully.")

if __name__ == "__main__":
    main()
