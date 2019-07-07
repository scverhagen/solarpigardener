#!/bin/bash
ifconfig
redis-server /etc/redis/redis.conf&
service nginx start&
celery -A app.celery worker&
uwsgi -s /tmp/uwsgi.sock --chmod-socket=666 --processes 4 --threads 2 --manage-script-name --mount /=app:app
