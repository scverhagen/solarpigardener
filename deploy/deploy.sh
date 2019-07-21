#!/bin/bash

echo This script will install solarpigardener on a fresh Raspbian installation.  Please run as root.  Please note that as of 7/13/2019 docker is still broken on Raspbian Buster.  Please use Raspbian Stretch for now.
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

# install and enable pigpio (remote GPIO server)
echo Installing pigpio remote GPIO server...
sudo apt-get install pigpio
sudo systemctl stop pigpiod

sudo rm -f /lib/systemd/system/pigpiod.service
sudo cat << 'EOF' >> /lib/systemd/system/pigpiod.service
[Unit]
Description=Daemon required to control GPIO pins via pigpio
[Service]
ExecStart=/usr/bin/pigpiod
ExecStop=/bin/systemctl kill pigpiod
Type=forking
[Install]
WantedBy=multi-user.target
EOF
sudo chmod 644 /lib/systemd/system/pigpiod.service
sudo systemctl daemon-reload
sudo systemctl unmask pigpiod
sudo systemctl enable pigpiod
sudo systemctl start pigpiod

# install solarpigardener docker container and systemd service:
echo Installing solarpigardener docker container and systemd service...
sudo rm -f /etc/systemd/system/solarpigardener.service
sudo cat << 'EOF' >> /etc/systemd/system/solarpigardener.service
[Unit]
Description=solarpigardener Container
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=30
Restart=always
ExecStart=/usr/bin/docker run -v /etc/gardener:/etc/gardener -p 80:80 scverhagen/solarpigardener
ExecStop=/usr/bin/docker stop scverhagen/solarpigardener

[Install]
WantedBy=multi-user.target
EOF
sudo chmod 644 /etc/systemd/system/solarpigardener.service
sudo systemctl enable solarpigardener
sudo systemctl start solarpigardener


# install watchtower docker container and systemd service:
echo Installing watchtower docker container and systemd service...
sudo rm -f /etc/systemd/system/watchtower.service
sudo cat << 'EOF' >> /etc/systemd/system/watchtower.service
[Unit]
Description=solarpigardener Container
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=60
Restart=always
ExecStart=/usr/bin/docker run -v /var/run/docker.sock:/var/run/docker.sock v2tec/watchtower:armhf-latest --cleanup
ExecStop=/usr/bin/docker stop v2tec/watchtower:armhf-latest

[Install]
WantedBy=multi-user.target
EOF
sudo chmod 644 /etc/systemd/system/watchtower.service
sudo systemctl enable watchtower
sudo systemctl start watchtower

# change hostname to 'solarpi'
echo Changing hostname to solarpi.
sudo hostname solarpi

#disable ipv6:
sudo echo " " >> /boot/cmdline.txt
echo "ipv6.disable=1" >> /boot/cmdline.txt

echo Installation complete!
read -p "Reboot (y, n)? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
    sudo reboot
fi
