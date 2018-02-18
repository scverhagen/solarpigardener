#!/bin/bash

# This script creates symlinks required for Solar Pi Gardener

scriptdir=$(dirname "$(readlink -f "$0")")
rootdir="$(dirname "$scriptdir")"

# set web root
webroot=$rootdir/webroot
ln -s $webroot /var/www/html/solarpi 


echo $rootdir
echo $scriptdir
echo $webroot

