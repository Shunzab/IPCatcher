#!/bin/bash
sudo echo "Installing IP Catcher service..."
sudo mkdir -p /opt/IPCatcher
sudo cp IPCatcher.py /opt/IPCatcher/
sudo cp IPCatcher.service /etc/systemd/system/
sudo chmod +x /opt/IPCatcher/IPCatcher.py
sudo systemctl daemon-reload
sudo systemctl enable IPCatcher
sudo systemctl start IPCatcher
sudo echo "Service installed and started."