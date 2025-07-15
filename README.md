An IP-monitoring script for both Windows (as a service using nssm) and Linux (as a systemd daemon). I’ve included downloadable template files and clear instructions—ready to zip up!

## Installation

1. Clone the repository:
```bash
git clone [https://github.com/Shunzab/IPCatcher]
cd [IPCatcher]
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
## Windows Package (nssm Service)

Files included:

    ip_monitor.py – your full Python script.

    install_service.bat – installs the service via nssm.

    uninstall_service.bat – removes the service cleanly.

Usage:

    Put all files (script + batch files) in C:\ip_monitor\.

    Run install_service.bat as Admin. It installs and starts the service.

    To stop and remove, run uninstall_service.bat.

## Linux Package (systemd Daemon)

Files included:

    ip_monitor.py – your script (make executable with chmod +x).

    ipmonitor.service – systemd service unit file.

    install.sh – installation script.

    uninstall.sh – removal script.

## 📦 Bundled Contents Summary:

windows/
├── ip_monitor.py
├── install_service.bat
└── uninstall_service.bat

linux/
├── ip_monitor.py
├── ipmonitor.service
├── install.sh
└── uninstall.sh

## ✅ Steps:
Platform	Action
Windows	Download/unzip under C:\ip_monitor, then run Install as Admin.
Linux	Upload/unzip under a user folder, then run sudo ./install.sh.

## Notes:
Also includes Extras if you wanna automate running from a single file as a service. Configuration.py is a file added later to configure app retriving timer, email address, and domain. Change before running. Orignal Files made cod also included. Use Task Scheduler To run the script on startup of your computer.
