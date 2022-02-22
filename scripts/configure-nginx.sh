#!/bin/bash
# Configures NGINX server at /etc/nginx/nginx.conf

# (Run from project root directory)
# Usage: sudo ./scripts/configure-nginx.sh

echo "Copying config over to /etc/nginx/nginx.conf.."
cat nginx.conf > /etc/nginx/nginx.conf
echo "Reloading NGINX.."
nginx -s reload
echo "Done! http://localhost"