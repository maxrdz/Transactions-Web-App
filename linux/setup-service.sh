#!/bin/bash
# Creates the systemd service for Flask.

# (Run from project root directory)
# Usage: sudo ./linux/create-service.sh

WORKING_DIR=$(pwd)
PYTHON_VENV=$WORKING_DIR/.venv/bin/python3.10
SYSTEMD=/etc/systemd/system
SERVICE=flask.service

cd $SYSTEMD
touch $SERVICE
echo "[Unit]
Description=Flask Web Server
After=network.target

[Service]
User=root
WorkingDirectory=$WORKING_DIR
ExecStart=$PYTHON_VENV -m webserver.Initialize
Restart=always

[Install]
WantedBy=multi-user.target" > $SERVICE

# Enable the Flask systemd service
systemctl unmask flask.service
systemctl enable flask.service
systemctl start flask.service
