import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from logger import *

load_dotenv()

def env_var_exist():
    if os.path.exists(".env"):
        pass
    else:    
        with open('.env', 'a') as env:
            pass


SENDER = os.getenv("EMAIL_SENDER")
RECIVER = os.getenv("EMAIL_RECEIVER")
PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(subject, body):
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