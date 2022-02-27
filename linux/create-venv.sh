#!/bin/bash
# Creates the Python virtual environment.

# (Run from project root directory)
# Usage: ./scripts/create-venv.sh

python -m venv .venv
.venv/bin/python3.10 -m pip install --upgrade pip
.venv/bin/python3.10 -m pip install -r requirements.txt
