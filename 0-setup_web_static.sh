#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static

# 1. Install Nginx if not already installed
if ! dpkg -l | grep -q nginx; then
    apt-get update -y
    apt-get install -y nginx
fi

# 2. Create required folders if they don't exist
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# 3. Create a fake HTML file to test Nginx configuration
echo "<html>
  <head>
  </head>
  <body>
    School
  </body>
</html>" > /data/web_static/releases/test/index.html

# 4. Create symbolic link (delete and recreate if it already exists)
if [ -L /data/web_static/current ]; then
    rm /data/web_static/current
fi
ln -s /data/web_static/releases/test/ /data/web_static/current

# 5. Give recursive ownership of /data/ to ubuntu user and group
chown -R ubuntu:ubuntu /data/

# 6. Update Nginx configuration to serve /hbnb_static/ using alias
nginx_config="/etc/nginx/sites-available/default"

# Check if the hbnb_static alias block is already configured to avoid duplication
if ! grep -q "location /hbnb_static" "$nginx_config"; then
    # Insert the location block right before the final closing brace of the server block
    sed -i '/server {/a \    location /hbnb_static {\n        alias /data/web_static/current/;\n    }' "$nginx_config"
fi

# 7. Restart Nginx
service nginx restart

exit 0
