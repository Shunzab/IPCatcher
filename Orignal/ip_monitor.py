import requests
from host_modifer import *
from logger import *
from send_email import *
import os
import platform
import time
import requests
from datetime import datetime

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org", timeout=10)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        log_error(f"[{timestamp()}] ERROR fetching IP: {e}")
        send_email("IP Monitor Error", f"Failed to get public IP.\n\n{e}")
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

