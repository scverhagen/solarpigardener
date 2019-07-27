#!/bin/bash
celery -A app.celery worker&
waitress-serve --listen 0.0.0.0:80 app:app
