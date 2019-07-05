#!/bin/bash
service nginx start&
uwsgi -s /tmp/uwsgi.sock --chmod-socket=666 --manage-script-name --mount /=app:app