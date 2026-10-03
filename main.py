import requests
import socket
import sys
from concurrent.futures import ThreadPoolExecutor

# ---------------------------------------------------------
# Block 1: Styling & Global Configurations
# ---------------------------------------------------------

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# Custom User-Agent prevents Web Application Firewalls (WAFs) from blocking default python-requests
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ReconLite/1.0"}


# ---------------------------------------------------------
# Block 2: File Loader
# ---------------------------------------------------------

def load_wordlist(filepath):
    """Reads a wordlist file safely and returns non-empty lines."""
    try:
        with open(filepath, "r") as f:
            words = [line.strip() for line in f if line.strip()]
        print(f"{Colors.GREEN}[*] Loaded {len(words)} entries from '{filepath}'{Colors.RESET}")
        return words
    except FileNotFoundError:
        print(f"{Colors.RED}[!] Error: File '{filepath}' not found.{Colors.RESET}")
        return []


# ---------------------------------------------------------
# Block 3: Subdomain Enumeration
# ---------------------------------------------------------

def check_subdomain(sub, domain):
    """Tests a single subdomain candidate."""
    url = f"http://{sub}.{domain}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=2, allow_redirects=False)
        if r.status_code in [200, 301, 302, 403]:
            print(f"  {Colors.GREEN}[+] [{r.status_code}] Found Subdomain: {url}{Colors.RESET}")
            return url
    except (requests.ConnectionError, requests.Timeout):
        pass
    return None


# ---------------------------------------------------------
# Block 4: Directory Enumeration
# ---------------------------------------------------------

def check_directory(entry, target_url):
    """Tests a single directory/file path candidate."""
    url = f"{target_url.rstrip('/')}/{entry}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=2, allow_redirects=False)
        if r.status_code in [200, 301, 302, 403]:
            print(f"  {Colors.GREEN}[+] [{r.status_code}] Found Directory: {url}{Colors.RESET}")
            return url
    except (requests.ConnectionError, requests.Timeout):
        pass
    return None


# ---------------------------------------------------------
# Block 5: Port Scanner
# ---------------------------------------------------------

def check_port(ip, port):
    """Attempts a TCP connection to a specific port."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))  # 0 indicates open port
        sock.close()

        if result == 0:
            print(f"  {Colors.GREEN}[+] Port {port} is OPEN{Colors.RESET}")
            return port
    except socket.error:
        pass
    return None


# ---------------------------------------------------------
# Block 6: CLI Wrappers & Action Handlers
# ---------------------------------------------------------

def run_subdomain_enum():
    domain = input("\nEnter target domain (e.g., example.com): ").strip()
    wordlist_path = input("Enter wordlist path: ").strip()

    words = load_wordlist(wordlist_path)
    if not words:
        return

    print(f"\n{Colors.CYAN}[*] Starting subdomain scan on '{domain}' with 20 threads...{Colors.RESET}\n")
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(lambda w: check_subdomain(w, domain), words)
    print(f"\n{Colors.BOLD}[*] Subdomain scan finished.{Colors.RESET}")


def run_directory_enum():
    target_url = input("\nEnter target URL (e.g., http://10.10.10.5): ").strip()
    wordlist_path = input("Enter wordlist path: ").strip()

    words = load_wordlist(wordlist_path)
    if not words:
        return

    print(f"\n{Colors.CYAN}[*] Starting directory scan on '{target_url}' with 20 threads...{Colors.RESET}\n")
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(lambda w: check_directory(w, target_url), words)
    print(f"\n{Colors.BOLD}[*] Directory scan finished.{Colors.RESET}")


def run_port_scan():
    target = input("\nEnter IP or hostname: ").strip()
    try:
        ip = socket.gethostbyname(target)
        if ip != target:
            print(f"{Colors.CYAN}[*] Resolved '{target}' to {ip}{Colors.RESET}")
    except socket.gaierror:
        print(f"{Colors.RED}[!] Could not resolve hostname '{target}'.{Colors.RESET}")
        return

    ports = range(1, 1025)  # Default ports 1-1024
    print(f"\n{Colors.CYAN}[*] Scanning ports 1-1024 on {ip} with 50 threads...{Colors.RESET}\n")
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(lambda p: check_port(ip, p), ports)
    print(f"\n{Colors.BOLD}[*] Port scan finished.{Colors.RESET}")


def show_banner():
    banner = f"""{Colors.CYAN}{Colors.BOLD}
 _____                     _     _ __     
|  __ \                   | |   (_) /     
| |__) |___  ___ ___  _ __| |    _| |_ ___ 
|  _  // _ \/ __/ _ \| '_ \ |   | | __/ _ \\
| | \ \  __/ (_| (_) | | | | |___| | ||  __/
|_|  \_\___|\___\___/|_| |_|______|_|\__\___|
{Colors.RESET}
  {Colors.BOLD}ReconLite - Fast Multi-Threaded Recon Toolkit{Colors.RESET}
  ==============================================
  1. Subdomain Enumeration
  2. Directory / File Discovery
  3. Fast Multi-Threaded Port Scanner
  4. Exit
  ----------------------------------------------"""
    print(banner)

# ---------------------------------------------------------
# Block 7: Main Menu Dispatcher Loop
# ---------------------------------------------------------

def main():
    actions = {
        "1": run_subdomain_enum,
        "2": run_directory_enum,
        "3": run_port_scan,
    }

    while True:
        show_banner()
        choice = input("Select an option (1-4): ").strip()

        if choice == "4":
            print(f"\n{Colors.GREEN}[*] Exiting ReconLite. Goodbye!{Colors.RESET}")
            sys.exit(0)
        elif choice in actions:
            actions[choice]()
        else:
            print(f"{Colors.RED}[!] Invalid choice. Please enter 1, 2, 3, or 4.{Colors.RESET}")


if __name__ == "__main__":
    main()
