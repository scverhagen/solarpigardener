#!/bin/bash
celery -A app.celery worker&
waitress-serve --listen *:80 app:app
