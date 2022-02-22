#!/bin/bash
# Copies over the files to the nginx server directory

# (Run from project root directory)
# Usage: sudo ./scripts/deploy-local-nginx.sh

echo "Copying website files to /data/www.."
cp -r www/* /data/www
echo "Copying resources to /data/images.."
cp -r images/* /data/images
echo "Reloading NGINX.."
nginx -s reload
echo "Done! http://localhost"