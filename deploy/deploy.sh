#!/bin/bash

echo This script will install solarpigardener on a fresh Raspbian installation.  Please note that as of 7/13/2019 docker is still broken on Raspbian Buster.  Please use Raspbian Stretch for now.
read -p "Continue? " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1 # handle exits from shell or function but don't exit interactive shell
fi

# install and enable docker:
echo Installing docker...
sudo apt-get install docker.io
sudo systemctl unmask docker
sudo systemctl enable docker
sudo systemctl start docker


# install and enable pigpio (remote GPIO server)
echo Installing pigpio (remote GPIO server)...
sudo apt-get install pigpio
sudo apt-get install unmask pigpiod
sudo systemctl enable pigpiod
sudo systemctl start pigpiod


# install solarpigardener docker container and systemd service:
echo Installing solarpigardener docker container and systemd service...
sudo cat << 'EOF' >> /etc/systemd/system/solarpigardener.service
[Unit]
Description=solarpigardener Container
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=0
Restart=always
ExecStart=/usr/bin/docker run -v /etc/gardener:/etc/gardener -p 80:80 scverhagen/solarpigardener

[Install]
WantedBy=multi-user.target
EOF
sudo chmod 644 /etc/systemd/system/solarpigardener.service
sudo systemctl enable solarpigardener
sudo systemctl start solarpigardener


# install watchtower docker container and systemd service:
echo Installing watchtower docker container and systemd service...
sudo cat << 'EOF' >> /etc/systemd/system/watchtower.service
[Unit]
Description=solarpigardener Container
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=30
Restart=always
ExecStart=/usr/bin/docker run -v /var/run/docker.sock:/var/run/docker.sock v2tec/watchtower:armhf-latest --cleanup

[Install]
WantedBy=multi-user.target
EOF
sudo chmod 644 /etc/systemd/system/watchtower.service
sudo systemctl enable watchtower
sudo systemctl start watchtower

# change hostname to 'solarpi'
echo Changing hostname to solarpi.
sudo hostname solarpi

echo Installation complete!
read -p "Reboot (y, n)? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
    sudo reboot
fi
