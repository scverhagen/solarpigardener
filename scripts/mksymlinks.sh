#!/bin/bash

# This script creates symlinks required for Solar Pi Gardener

scriptdir=$(dirname "$(readlink -f "$0")")
rootdir="$(dirname "$scriptdir")"

# set web root
webroot=$rootdir/webroot
ln -s $webroot /var/www/html/gardener
ln -s $rootdir/index.php /var/www/html/index.php

# create symlink for sending commands to gardener daemon
ln -s /tmp/gardener.cmd $webroot/gardener.cmd
chmod 0777 $webroot/gardener.cmd

echo $rootdir
echo $scriptdir
echo $webroot

