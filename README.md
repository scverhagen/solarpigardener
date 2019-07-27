# solarpigardener
<h4>Automated self-watering garden system controlled by a solar-powered raspberry Pi.</h4>
<br>
<h4>Installation (to a Raspberry Pi) using script</h4>
Please note that as of 7/2019 docker is broken in Raspian Buster.  Until the issue is fixed, Raspian Stretch should be used.<br>
1.  Install Raspbian Stretch, enable ssh, and change default password.<br>
2.  From a bash terminal, type:<br>
<pre>
wget https://raw.githubusercontent.com/scverhagen/solarpigardener/production/deploy/deploy.sh <br>
chmod +x ./deploy.sh<br>
sudo deploy.sh<br>
sudo reboot<br>
</pre>
<br>
The script will install Docker, docker-compose, solarpigardener and watchtower (for automatic updates).
