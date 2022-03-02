#!/bin/bash
# Starts the Flask web server.

# (Run from project root directory)
# Usage: ./scripts/launch-server.sh

ENVIRONMENT=.venv/bin/python3.10
sudo ./$ENVIRONMENT -m webserver.Initialize
