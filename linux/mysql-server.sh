#!/bin/bash
# Starts the Percona (MySQL) database server.

# (Run from project root directory)
# Usage: ./scripts/mysql-server.sh

if [ ! -d "/var/lib/mysql" ]; then
    sudo mkdir /data/lib/mysql
fi
if [ ! -d "/var/lib/mysql-files" ]; then
    sudo mkdir /data/lib/mysql-files
fi
# Check that data directories are initialized
sudo mysqld --initialize
# Start MySQL database daemon
sudo mysqld