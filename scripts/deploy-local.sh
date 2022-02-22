#!/bin/bash
# Copies over the files to the nginx server directory

# (Run from project root directory)
# Usage: sudo ./scripts/deploy-local-nginx.sh

if [ -d "/data" ]; then
    rm -rf /data
fi
mkdir /data
mkdir /data/www
mkdir /data/resources

echo "Copying website files to /data/www.."
cp -r www/* /data/www
echo "Copying resources to /data/resources.."
cp -r resources/* /data/resources
echo "Reloading NGINX.."
nginx -s reload
echo "Done! http://localhost"