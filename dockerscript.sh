#!/bin/bash
python3 ./app/gardener_daemon.py
service nginx start
uwsgi -s /tmp/uwsgi.sock --chmod-socket=666 --manage-script-name --mount /=app:app