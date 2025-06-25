import os
import platform
import time
import requests
from datetime import datetime
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import ctypes

load_dotenv()


def env_var_exist():
    if os.path.exists(".env"):
        pass
    else:    
        with open('.env', 'a') as env:
            env.write("EMAIL_SENDER = \"\"\n")
            env.write("EMAIL_PASSWORD = \"\"\n")
            env.write("EMAIL_RECEIVER = \"\"\n")



def interval_domain(inte, dom):
    global CHECK_INTERVAL
    global HOST_ENTRY_NAME

    CHECK_INTERVAL  = inte
    HOST_ENTRY_NAME = dom

CHECK_INTERVAL = 1800  # 30 mins
HOST_ENTRY_NAME = "my_home"


CHANGE_LOG_FILE = "ip_change_log.txt"
ERROR_LOG_FILE = "ip_error_log.txt"


SENDER = os.getenv("EMAIL_SENDER")
RECEIVER = os.getenv("EMAIL_RECEIVER")
PASSWORD = os.getenv("EMAIL_PASSWORD")


def is_admin():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def get_hosts_file_path():
    if platform.system() == "Windows":
        return r"C:\Windows\System32\drivers\etc\hosts"
    else:
        return "/etc/hosts"

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org", timeout=10)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        log_error(f"[{timestamp()}] ERROR fetching IP: {e}")
        send_email("IP Monitor Error", f"Failed to get public IP.\n\n{e}")
        return None

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def send_email(subject, body):
    if not SENDER or not RECEIVER or not PASSWORD:
        print("[ERROR] Email credentials are missing in .env file. Email not sent.")
        return
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = SENDER
        msg['To'] = RECEIVER

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER, PASSWORD)
            server.send_message(msg)
    except Exception as e:
        log_error(f"Failed to send email:{e}")

def log_change(ip):
    entry = f"[{timestamp()}] IP changed to: {ip}"
    with open(CHANGE_LOG_FILE, 'a') as f:
        f.write(entry + "\n")
    print(entry)
    send_email("Public IP Changed", entry)

def log_error(msg):
    print(msg)
    with open(ERROR_LOG_FILE, 'a') as f:
        f.write(msg + "\n")

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

def monitor_ip():
    print("[INFO] Starting IP monitor that updates the hosts file...")
    while True:
        current_ip = get_public_ip()
        if current_ip:
            hosts_ip = get_current_hosts_ip()
            if current_ip != hosts_ip:
                update_hosts_file(current_ip)
            else:
                print(f"[INFO] No change. Current IP still: {current_ip}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    if not is_admin():
        print("[ERROR] This script must be run as root/administrator to modify the hosts file.")
        exit(1)
    monitor_ip()
    env_var_exist()