CHANGE_LOG_FILE = "ip_change_log.txt"
ERROR_LOG_FILE = "ip_error_log.txt"

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