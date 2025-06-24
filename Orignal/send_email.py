import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from logger import *

load_dotenv()

def env_var_exist():
    if not os.path.exists(".env"):
        with open('.env', 'w') as env:
            env.write("EMAIL_SENDER=\nEMAIL_PASSWORD=\nEMAIL_RECEIVER=\n")


SENDER = os.getenv("EMAIL_SENDER")
RECEIVER = os.getenv("EMAIL_RECEIVER")
PASSWORD = os.getenv("EMAIL_PASSWORD")

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