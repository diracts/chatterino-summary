import os
import sys
import getpass
import re
from datetime import datetime

def filename_to_date(filename: str) -> datetime: 
    """Convert filename like "hasanabi-2023-10-14.log" to "10-14-2023".

    Args:
        filename (str): Filename to convert.

    Returns:
        str: Date in format "MM-DD-YYYY".
    """
    filename = filename.split(".")[0]
    filename = filename.split("-")
    filename = f"{filename[2]}-{filename[3]}-{filename[1]}"
    date = datetime.strptime(filename, "%m-%d-%Y")
    return date

def find_min_date(filename_date_dict: dict) -> datetime:
    """Find the earliest date in a dictionary of filenames and dates.

    Args:
        filename_date_dict (dict): Dictionary of filenames and dates.

    Returns:
        datetime.datetime: Earliest date.
    """
    min_date = datetime.now()
    for filename in filename_date_dict:
        if filename_date_dict[filename] < min_date:
            min_date = filename_date_dict[filename]
    return min_date

def find_max_date(filename_date_dict: dict) -> datetime:
    """Find the latest date in a dictionary of filenames and dates.

    Args:
        filename_date_dict (dict): Dictionary of filenames and dates.

    Returns:
        datetime.datetime: Latest date.
    """
    max_date = datetime(1970, 1, 1)
    for filename in filename_date_dict:
        if filename_date_dict[filename] > max_date:
            max_date = filename_date_dict[filename]
    return max_date

def count_chats(filename: str, username: str) -> int:
    """Count the number of times a username has chatted in a log file.

    Args:
        filename (str): Log file to search.
        username (str): Username to search for.

    Returns:
        int: Number of times the username has chatted in the log file.
    """
    username_regex = re.compile(rf"\[\d\d:\d\d:\d\d\] +{username}:")
    with open(filename, "r") as f:
        lines = f.readlines()
    count = 0
    for line in lines:
        if username_regex.search(line):
            count += 1
    return count

# >>> Detecting your username <<<
# This is necessary to find the location of the chatterino logs.
USERNAME = getpass.getuser()
print(f"[ ] Username: {USERNAME}")

# >>> Detecting your operating system <<<
# This is necessary to find the location of the chatterino logs. 
OS = sys.platform
if OS == "win32":
    print("[ ] OS is Windows")
    OS_NAME = "windows"
elif OS == "linux" or OS == "linux2":
    print("[ ] OS is Linux")
    OS_NAME = "linux"
elif OS == "darwin":
    print("[ ] OS is MacOS")
    OS_NAME = "macos"
else:
    print("[-] Could not detect OS.")
    print(f"[ DEBUG ] OS: {OS}")
    print(f"[-] Exiting...")
    sys.exit(1)

if OS_NAME == "macos":
    LOGS_PATH = f"{os.environ['HOME']}/Library/Application Support/chatterino/Logs/Twitch/Channels"

# Get list of directories in LOGS_PATH

print(f"[ ] Logs path: {LOGS_PATH}")

channel_list = os.listdir(LOGS_PATH)
channel_list.remove(".DS_Store")

print(f"[ ] Channels:")
for channel in channel_list:
    print(f"[ ]     {channel}")

# >>> Get user input for channel <<<

channel = input("[+] Enter channel name: ")
if channel in channel_list:
    print(f"[ ] Now looking in the logs for {channel}'s channel...")
else:
    print(f"[-] ERROR: Could not find log files for {channel}.")
    print(f"[-] Exiting...")
    sys.exit(1)


# >>> Get list of log files for channel <<<
log_files = os.listdir(f"{LOGS_PATH}/{channel}")

filename_date_dict = {}
for filename in log_files:
    filename_date_dict[filename] = filename_to_date(filename)

min_date = find_min_date(filename_date_dict)
max_date = find_max_date(filename_date_dict)
number_of_files = len(filename_date_dict)

if number_of_files == 1:
    print(f"[ ] Found 1 log file for the date: {min_date.strftime('%d %B %Y')}")
else:
    print(f"[ ] Found {number_of_files} log files for the range: {min_date.strftime('%d %B %Y')} to {max_date.strftime('%d %B %Y')}")

while True:
    print("[ ] How do you want to search these files? Please select which mode you want:")
    print("[ ]     A - Search all files")
    print("[ ]     R - Search a specific date range")
    print("[ ]     S - Search a specific date")
    print("[ ]     Q - Quit")

    mode = input("[+] Enter mode: ")
    mode = mode.upper()
    if mode == "A":
        print("[ ] Searching all files.")
        break
    elif mode == "R":
        print("[ ] Searching a specific date range.")
        break
    elif mode == "S":
        print("[ ] Searching a specific date.")
        break
    elif mode == "Q":
        print("[ ] Quitting...")
        sys.exit(0)
    else:
        print("[-] ERROR: Invalid mode. Try again.")
        continue

# If mode == A, then we don't need to do anything.
# If mode == R, then we need to ask for a start and end date.
# If mode == S, then we need to ask for a specific date.

if mode == "R":
    while True:
        start_date = input("[+] Enter start date (MM-DD-YYYY): ")
        try:
            start_date = datetime.strptime(start_date, "%m-%d-%Y")
            break
        except ValueError:
            print("[-] ERROR: Invalid date. Try again.")
            continue
    while True:
        end_date = input("[+] Enter end date (MM-DD-YYYY): ")
        try:
            end_date = datetime.strptime(end_date, "%m-%d-%Y")
            break
        except ValueError:
            print("[-] ERROR: Invalid date. Try again.")
            continue
    if start_date > end_date:
        print("[-] ERROR: Start date is after end date. Try again.")
        sys.exit(1)

    # Remove all files that are not in the date range
    for filename in list(filename_date_dict):
        if filename_date_dict[filename] < start_date or filename_date_dict[filename] > end_date:
            filename_date_dict.pop(filename)


if mode == "S":
    while True:
        specific_date = input("[+] Enter date (MM-DD-YYYY): ")
        try:
            specific_date = datetime.strptime(specific_date, "%m-%d-%Y")
            break
        except ValueError:
            print("[-] ERROR: Invalid date. Try again.")
            continue

    # Remove all files that are not on the specific date
    for filename in list(filename_date_dict):
        if filename_date_dict[filename] != specific_date:
            filename_date_dict.pop(filename)


min_date = find_min_date(filename_date_dict)
max_date = find_max_date(filename_date_dict)
number_of_files = len(filename_date_dict)

if number_of_files == 1:
    print(f"[ ] Found 1 log file for the date: {min_date.strftime('%d %B %Y')}")
else:
    print(f"[ ] Found {number_of_files} log files for the range: {min_date.strftime('%d %B %Y')} -> {max_date.strftime('%d %B %Y')}")

if min_date == max_date:
    print("[-] WARNING: Only one log file found.")


# Ask for what twitch username to search for
twitch_username = input("[+] Enter username to search for: ")
twitch_username = twitch_username.lower()

total_messages = 0

for filename in filename_date_dict:
    messages = count_chats(LOGS_PATH + '/' + channel + '/' + filename, twitch_username)
    total_messages += messages
    print(f"[ ]     {filename} - {messages}")

print(f"[ ] Total messages: {total_messages}")