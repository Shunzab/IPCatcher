from IPCatcher import *

def get_email_address(send, recv, pwd):
        with open('.env' , 'w') as env:
            env.write(f"EMAIL_SENDER = {send}\nEMAIL_PASSWORD = {pwd}\nEMAIL_RECEIVER ={recv}")

def interval_domain(inte, dom):
    global CHECK_INTERVAL
    global HOST_ENTRY_NAME

    CHECK_INTERVAL  = inte
    HOST_ENTRY_NAME = dom


def skip():
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
        skip()

    a = int(input("Please enter the interval(in seconds) after which IP is checked for again or press enter for default timer(Half Hour):"))
    b = input("Please enter your domain name or press enter for default(home.home):")
    if type(a) is int:
        interval_domain(a, b)
    else:
        print('Using Default timer!')
        interval_domain(1800, b)

if __name__ == "__main__":
	skip()