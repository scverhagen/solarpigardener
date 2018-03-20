#!/bin/bash
scriptdir=$(dirname "$(readlink -f "$0")")

systemctl stop gardener
cp $scriptdir/../systemd/gardener.service /etc/systemd/system/gardener.service
systemctl daemon-reload
systemctl enable gardener
systemctl start gardener
