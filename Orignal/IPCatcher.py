import os
from host_modifer import *
from ip_monitor import *
from send_email import *
from logger import *

def clear_screen(): 
    os.system('cls' if os.name == 'nt' else 'clear')

BOLD = '\033[1m'
END = '\033[0m'

print(f"{BOLD}PLEASE RUN THIS COD WITH ADMINISTATOR(SUDO IN LINUX) PRIVELIGES. TO CONFIGURE YOUR DYNAMIC-DNS, IT MAKES CHANGES TO HOST FILE. BEWARE!{END}")
print("****************************************WELCOME TO IP CATCHER!!!****************************************")
menu=(                               '*******************MENU*******************'                               ).center(101)
options = ("1- Run as a program.\n                              2-Run as a service.").center(130)
print(menu)
print(f"{options}")

def get_email_address(send, recv, pwd):
        with open('.env' , 'w') as env:
            env.write(f"EMAIL_SENDER = {send}\n EMAIL_PASSWORD = {pwd}\n EMAIL_RECEIVER ={recv}")


def service_runner():
    if platform.system() == "Windows":
        print('You are using a Windows machine. Go to Windows_Service folder and RUN install/uninstall.bat AS ADMINISTATOR!')
    else:
        print('You are using a Linux machine. Go to linux_daemon folder and RUN install/uninstall.sh as AS SUDO!')


def your_choice():
    choice = int(input("Please enter your choice...\n"))

    if choice == 1:
            skip = input("Do you want to set email alerts(y/n):")
            if skip == 'y':
                env_var_exist()
                x = input("Please enter the email address you wanna send email from:")
                y = input("Please enter the app password of the email address you wanna send email from:")
                z = input("Please enter the email address you wanna send email to:")
                get_email_address(x, y, z)
            elif skip == 'n':
                monitor_ip()
            else:
                print('Invalid Choice!')
                your_choice()

            a = input("Please enter the interval(in seconds) after which IP is checked for again or press enter for default timer(Half Hour):") # it uses default value if anything other than an integer is used.
            b = input("Please enter your domain name or press enter for default(home.home):") or "home.home"
            try:
                interval = int(a)
            except (ValueError, TypeError):
                interval = 1800
            interval_domain(interval, b)
            monitor_ip()
    elif choice == 2:
        service_runner()
    else:
        print('Invalid Choice!')
        your_choice()


if __name__ == "__main__":
    your_choice()




