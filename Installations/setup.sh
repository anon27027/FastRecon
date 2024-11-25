#!/bin/bash

# Directory to save installations
INSTALL_DIR="Installations"
LOG_FILE="install.log"
mkdir -p "$INSTALL_DIR"

# Python modules required for the script
PYTHON_MODULES=(
    "requests"
    "argparse"
    "whois"
    "waymore"
    "gau-python"
)

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install Python dependencies
install_python_modules() {
    echo "[*] Installing Python modules..." | tee -a "$LOG_FILE"
    
    # Install or check each Python module
    for module in "${PYTHON_MODULES[@]}"; do
        pip show "$module" >/dev/null 2>&1
        if [ $? -ne 0 ]; then
            sudo pip install "$module" || { echo "[!] Failed to install Python module: $module."; exit 1; }
            echo "[+] Installed Python module: $module" | tee -a "$LOG_FILE"
        else
            echo "[*] Python module '$module' is already installed." | tee -a "$LOG_FILE"
        fi
    done
}

# Check if pip is installed
if ! command_exists pip; then
    echo "[!] pip is not installed. Please install pip first."
    exit 1
fi

# Install Python dependencies
install_python_modules

echo "[+] All installations completed successfully."
# Call the Python script
echo "[*] Running install_tools.py..."
python3 Installations/install_tools.py
