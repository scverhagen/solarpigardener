#!/bin/bash
ifconfig
redis-server /etc/redis/redis.conf&
celery -A app.celery worker&
waitress-serve --listen *:80 app:app
