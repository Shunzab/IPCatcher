import os
import platform
import time
from datetime import datetime
from send_email import *
from logger import *


CHECK_INTERVAL = 1800  # 30 mins default
HOST_ENTRY_NAME = "home.home"

def interval_domain(inte, dom):
    global CHECK_INTERVAL
    global HOST_ENTRY_NAME

    CHECK_INTERVAL  = inte
    HOST_ENTRY_NAME = dom

def get_hosts_file_path():
    if platform.system() == "Windows":
        return r"C:\Windows\System32\drivers\etc\hosts"
    else:
        return "/etc/hosts"


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_hosts_file():
    path = get_hosts_file_path()
    try:
        with open(path, 'r') as f:
            return f.readlines()
    except Exception as e:
        error = f"[{timestamp()}] Failed to read hosts file: {e}"
        log_error(error)
        send_email("Hosts File Error", error)
        return None


def write_hosts_file(lines):
    path = get_hosts_file_path()
    try:
        with open(path, 'w') as f:
            f.writelines(lines)
    except Exception as e:
        error = f"[{timestamp()}] Failed to write hosts file: {e}"
        log_error(error)
        send_email("Hosts File Error", error)

        
def update_hosts_file(ip):
    lines = read_hosts_file()
    if lines is None:
        return

    updated = False
    new_lines = []
    for line in lines:
        if HOST_ENTRY_NAME in line and not line.strip().startswith("#"):
            new_lines.append(f"{ip}\t{HOST_ENTRY_NAME}\n")
            updated = True
        else:
            new_lines.append(line)

    if not updated:
        new_lines.append(f"{ip}\t{HOST_ENTRY_NAME}\n")
        updated = True

    write_hosts_file(new_lines)
    log_change(ip)

    
def get_current_hosts_ip():
    lines = read_hosts_file()
    if lines is None:
        return None
    for line in lines:
        if HOST_ENTRY_NAME in line and not line.strip().startswith("#"):
            return line.strip().split()[0]
    return None