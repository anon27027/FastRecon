#!/usr/bin/env python3

import os
import sys

class Colors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

def print_banner():
    banner = """
    ███████╗ █████╗ ███████╗██╗   ██╗██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
    ██╔════╝██╔══██╗██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
    █████╗  ███████║███████╗ ╚████╔╝ ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
    ██╔══╝  ██╔══██║╚════██║  ╚██╔╝  ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
    ███████╗██║  ██║███████║   ██║   ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
    ╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
    """
    print(f"{Colors.CYAN}{banner}{Colors.RESET}")
    print(f"{Colors.GREEN}Version 1.0 - Your All-in-One Reconnaissance Framework{Colors.RESET}\n")

def show_menu():
    menu_items = {
        1: ("Subdomain Finder", "SubdomainFinder/main.py"),
        2: ("Port Scanner", "PortScanner/main.py"),
        3: ("Screenshotting", "modules/screenshot.py"),
        4: ("Links Finder", "LinksFinder/main.py"),
        5: ("Parameter Discovery", "ParameterFinder/main.py"),
        6: ("Fuzzing", "modules/fuzzing.py"),
        7: ("CMS Identification", "modules/cms_identify.py"),
        8: ("Vulnerability Scanners", "modules/vuln_scanner.py"),
        9: ("Content Discovery", "modules/content_discovery.py"),
        10: ("Lookup Tools", "Lookup")
    }

    print(f"{Colors.YELLOW}Select an option:{Colors.RESET}")
    for key, (name, _) in menu_items.items():
        print(f"{Colors.BLUE}[{key}] {name}{Colors.RESET}")
    print(f"{Colors.RED}[0] Exit{Colors.RESET}")
    print(f"{Colors.RED}[q] Quick Exit (Immediately terminate){Colors.RESET}\n")

    try:
        choice = input(f"{Colors.GREEN}Enter your choice: {Colors.RESET}").lower()
        
        if choice == 'q':
            print(f"{Colors.YELLOW}Terminating immediately...{Colors.RESET}")
            sys.exit(0)
        
        if choice == '0':
            print(f"{Colors.YELLOW}Thank you for using EasyRecon. Goodbye!{Colors.RESET}")
            sys.exit(0)
            
        choice = int(choice)
        if choice in menu_items:            
            module_path = menu_items[choice][1]
           
            if os.path.exists(module_path):
                if choice == 1:
                    domain = input("Enter the Domain Name: ")
                    os.system(f'python3 {module_path} -t {domain}')
                elif choice == 2:
                    inp = input("Enter IP Range/IP Address/Domain Name: ")
                    level = int(input("Scan Level 1(Slow and Robust) \nScan Level 2 (Fast and Lean): "))

                    l = ["S", "F"]
                    os.system(f'python3 {module_path} {inp} {l[level-1]}')
                elif choice == 4:
                    domain = input("Enter the Domain Name: ")

                    level = int(input("Scan Level 1(Slow and Robust) \nScan Level 2 (Fast and Lean): "))

                    l = ["S", "F"]

                    os.system(f'python3 {module_path} {domain} {l[level-1]}')
                elif choice == 5:
                    domain = input("Enter the Domain Name: ")

                    os.system(f'python3 {module_path} {domain}')

                elif choice == 10:
                    inp = input("Enter IP Address/Domain Name: ")

                    print("Domain Based LookUP")

                    os.system(f'python3 {module_path}/DomainBased/main.py -t {inp}')

                    print("IP Based LookUP")

                    os.system(f'python3 {module_path}/IPBased/maliciousIP.py -t {inp}')

                    os.system(f'python3 {module_path}/IPBased/location.py -t {inp}')                    

            else:
                print(f"{Colors.RED}Module not implemented yet!{Colors.RESET}")
        else:
            print(f"{Colors.RED}Invalid choice!{Colors.RESET}")
    except ValueError:
        if choice not in ['0', 'q']:
            print(f"{Colors.RED}Please enter a valid number!{Colors.RESET}")
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted by user. Exiting...{Colors.RESET}")
        sys.exit(0)

def main():
    try:
        while True:
            os.system('clear' if os.name == 'posix' else 'cls')
            print_banner()
            show_menu()
            input(f"\n{Colors.CYAN}Press Enter to continue or Ctrl+C to exit...{Colors.RESET}")
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Thank you for using EasyRecon. Goodbye!{Colors.RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()