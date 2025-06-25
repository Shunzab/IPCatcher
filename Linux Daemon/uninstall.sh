#!/bin/bash
sudo echo "Removing IP Catcher service..."
sudo systemctl stop IPCatcher
sudo systemctl disable IPCatcher
sudo rm -rf /etc/systemd/system/IPCatcher.service
sudo systemctl daemon-reload
sudo rm -rf /opt/IPCatcher
sudo rm -rf /opt/IPCatcher/.env
sudo echo "Service removed."