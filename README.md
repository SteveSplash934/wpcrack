# WPCrack

WPCrack is a Python script designed for ethical penetration testing to crack WordPress login pages. It allows you to attempt to crack a WordPress target or a list of targets using specified usernames and passwords. The script supports various export formats for results and provides options for both single and list-based input.

## Features

- Crack WordPress login pages using specified usernames and passwords.
- Support for single or list-based usernames and passwords.
- Export results in JSON, CSV, or TXT formats.
- Specify output filename for results.
- Ethical use only.

## Installation

To use WPCrack, you'll need to have Python 3.6+ installed on your system. Install the required packages using pip:

```bash
pip install -r requirements.txt
```

## Usage

Run the script from the command line with the following options:

```
usage: wp_crack.py [-h] [-u USERNAME] [-U USERNAME_LIST] [-p PASSWORD] [-P PASSWORD_LIST] [-t TARGET] [-T TARGETS] [-v] [--update] [-x {json,csv,txt}] [-o OUTPUT]

WPCrack attempts to crack a WordPress target or list of targets using a defined username and password or a list of usernames and passwords

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Specify a single username
  -U USERNAME_LIST, --username-list USERNAME_LIST
                        Specify a username list
  -p PASSWORD, --password PASSWORD
                        Specify a single password
  -P PASSWORD_LIST, --password-list PASSWORD_LIST
                        Specify a password list
  -t TARGET, --target TARGET
                        Specify a single target
  -T TARGETS, --Targets TARGETS
                        Specify a target list
  -v, --version         Print the version
  --update              Update the software
  -x {json,csv,txt}, --export {json,csv,txt}
                        Specify the format for export results
  -o OUTPUT, --output OUTPUT
                        Specify the output filename for results
```

### Examples

1. **Single username and password**

   ```bash
   python wp_crack.py -u admin -p password123 -t http://example.com/wp-login.php
   ```

2. **Username and password list**

   ```bash
   python wp_crack.py -U usernames.txt -P passwords.txt -T targets.txt
   ```

3. **Export results to CSV**

   ```bash
   python wp_crack.py -u admin -p password123 -t http://example.com/wp-login.php -x csv -o results.csv
   ```

## Update

To update the software, use the `--update` flag:

```bash
python wp_crack.py --update
```

## Upcoming Features

We are working on adding more features to enhance the functionality of WPCrack. Upcoming updates include:

- **Random User-Agents**: Support for randomizing user-agent headers to improve stealth and mimic different clients.
- **Captcha Bypass**: Integration with techniques to bypass common CAPTCHA challenges encountered during login attempts.
- **Multithreading**: Implementation of multithreading to speed up the cracking process by making concurrent attempts.
- **Software Update**: Improved and automated update mechanism to ensure you always have the latest version.

## License

This script is intended for ethical use only. Use it responsibly and ensure you have proper authorization before attempting to crack any WordPress login pages.

## Disclaimer

The author is not responsible for any misuse or damage caused by the use of this software. Ensure you have permission before conducting any security testing.
