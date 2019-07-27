#!/bin/bash

echo This script will install solarpigardener on a fresh Raspbian installation.  Please note that as of 7/13/2019 docker is still broken on Raspbian Buster.  Please use Raspbian Stretch for now.
read -p "Continue? (y,n)" -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1 # handle exits from shell or function but don't exit interactive shell
fi

# install and enable docker:
echo Installing docker...
sudo apt-get remove docker docker-engine docker.io containerd runc
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

sudo systemctl unmask docker
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER

# install docker-compose (using pip)
sudo apt-get install python3 python3-pip
sudo pip3 install docker-compose

# install solarpigardener docker container and systemd service:
echo Installing solarpigardener docker container and systemd service...
sudo rm -f /etc/systemd/system/solarpigardener.service
sudo cat << 'EOF' >> /etc/systemd/system/solarpigardener.service
[Unit]
Description=solarpigardener
Requires=docker.service
After=docker.service
[Service]
Restart=always
User=root
Group=docker
ExecStartPre=/usr/bin/docker-compose -f /home/pi/solarpigardener/docker-compose.yml down -v
ExecStart=/usr/bin/docker-compose -f /home/pi/solarpigardener/docker-compose.yml up
ExecStop=/usr/bin/docker-compose -f /home/pi/solarpigardener/docker-compose.yml down -v
[Install]
WantedBy=multi-user.target
EOF

sudo chmod 644 /etc/systemd/system/solarpigardener.service
sudo systemctl enable solarpigardener
sudo systemctl start solarpigardener

echo "Please use the raspi-config tool to enable remote GPIO."
read -n 1 -s -r -p "Press any key to continue"
sudo raspi-config

# change hostname to 'solarpi'
echo Changing hostname to solarpi.
sudo hostname solarpi

echo Installation complete!
read -p "Reboot (y, n)? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
    sudo reboot
fi
