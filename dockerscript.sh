#!/bin/bash
service nginx start&
GPIOZERO_PIN_FACTORY=pigpio PIGPIO_ADDR=host.docker.internal uwsgi -s /tmp/uwsgi.sock --chmod-socket=666 --processes 4 --threads 2 --manage-script-name --mount /=app:app
