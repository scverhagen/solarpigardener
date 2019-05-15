#!/bin/bash
systemctl stop gardener
cp gardener.service /etc/systemd/system/gardener.service
systemctl daemon-reload
systemctl enable gardener
systemctl start gardener
