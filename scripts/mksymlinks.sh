#!/bin/bash

# This script creates symlinks required for Solar Pi Gardener

scriptdir=$(dirname "$(readlink -f "$0")")
rootdir="$(dirname "$scriptdir")"

# set web root
webrootdir=$rootdir/webroot
if [ ! -L /var/www/html/gardener ]; then
	ln -s $webrootdir /var/www/html/gardener
fi

if [ ! -L /var/www/html/index.php ]; then
	ln -s $rootdir/index.php /var/www/html/index.php
fi

#echo $rootdir
#echo $scriptdir
#echo $webrootdir

