#!/usr/bin/env bash
# sets up the web servers for the deployment of web_static

# Install Nginx if not already installed
if ! [ -x "$(command -v nginx)" ]; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# Create the necessary directories
sudo mkdir -p /data/web_static/{releases/test,shared}

# Create a fake HTML file for testing
echo "Hello World!" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create a symbolic link
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Give ownership of the /data/ folder to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration
sudo sed -i '/^\s*server\s*{/a \\\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart
