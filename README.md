# solarpigardener
<h4>Automated self-watering garden system controlled by a solar-powered raspberry Pi.</h4>
<br>
<h4>Installation (to a Raspberry Pi) using script</h4>
1.  Install Raspbian Stretch, enable ssh, and change default password.<br><br>
2.  From a bash terminal, type:<br>
<code>
wget https://raw.githubusercontent.com/scverhagen/solarpigardener/production/deploy/deploy.sh
chmod +x ./deploy.sh
sudo deploy.sh
sudo reboot
</code>
<br>
The script will install Docker, solarpigardener and watchtower (for automatic updates).
