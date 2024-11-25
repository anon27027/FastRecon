import argparse
import subprocess
from pathlib import Path
from threading import Thread

def clean_text(text):
    """
    Cleans the text by removing unnecessary whitespace and lines.
    Customize this function based on the specific output of `arjun`.
    """
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())

def process_subdomain(subdomain, output_file):
    """Run the `arjun` command for a single subdomain and write cleaned output to the file."""
    try:
        print(f"Running arjun for {subdomain}...")
        # Run the arjun command and capture output
        result = subprocess.run(
            ["arjun", "-u", subdomain],
            text=True, capture_output=True, check=True
        )
        # Clean the output
        cleaned_output = clean_text(result.stdout)
        if cleaned_output:  # Only write non-empty results
            with output_file.open('a') as outfile:
                outfile.write(f"Results for {subdomain}:\n")
                outfile.write(cleaned_output + "\n")
                outfile.write("-" * 80 + "\n")
    except subprocess.CalledProcessError as e:
        print(f"Error processing {subdomain}: {e}")
    except Exception as e:
        print(f"Unexpected error for {subdomain}: {e}")

def run_arjun(domain):
    # Convert file paths to Path objects for safe handling
    subdomain_path = Path(f"logs/{domain}/subdomain.txt")
    output_path = Path(f"logs/{domain}/parameters.txt")

    # Check if the subdomain file exists
    if not subdomain_path.exists():
        print(f"Error: File does not exist. Run Subdomain Finder first.")
        return

    # Read subdomains from the file
    with subdomain_path.open('r') as infile:
        subdomains = [line.strip() for line in infile if line.strip()]

    # Clear the output file or create it if it doesn't exist
    output_path.touch(exist_ok=True)
    output_path.write_text("")  # Clear file content

    threads = []

    # Create and start a thread for each subdomain
    for subdomain in subdomains:
        thread = Thread(target=process_subdomain, args=(subdomain, output_path))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

def main():
    parser = argparse.ArgumentParser(description="Run arjun on a list of subdomains.")
    parser.add_argument(
        "domain",
        help="Domain Name",
    )
    
    args = parser.parse_args()

    run_arjun(args.domain)

if __name__ == "__main__":
    main()
