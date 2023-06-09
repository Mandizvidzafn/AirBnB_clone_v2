#!/usr/bin/env bash
# sets up the web servers for the deployment of web_static

# Install Nginx if not already installed
if ! [ -x "$(command -v nginx)" ]; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# Create the necessary directories
if sudo mkdir -p /data/web_static/{releases/test,shared}; then
    echo "Directories created successfully"
else
    echo "Error: Failed to create directories"
fi

# Create a fake HTML file for testing
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create a symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration
if ! grep -q '/hbnb_static/' /etc/nginx/sites-available/hello; then
    sudo sed -i '/^\s*server\s*{/a \
        location /hbnb_static/ {\
            alias /data/web_static/current/;\
        }\
    ' /etc/nginx/sites-available/hello
fi


#Create a symbolic link fro default sites-available and enabled
sudo ln -sf /etc/nginx/sites-available/hello /etc/nginx/sites-enabled/hello

# Test Nginx
sudo nginx -t

# Restart Nginx
sudo service nginx restart
