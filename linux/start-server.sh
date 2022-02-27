#!/bin/bash
# Starts the CherryPy web server.

# (Run from project root directory)
# Usage: ./scripts/start-server.sh

ENVIRONMENT=.venv/bin/python3.10
./$ENVIRONMENT -m webserver.Initialize