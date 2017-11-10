#!/usr/bin/env bash
git pull
kill $(ps aux | grep 'final-project' | awk '{print $2}')
nohup gunicorn --certfile cert.pem --keyfile key.pem --worker-class eventlet -w 1 -b 0.0.0.0:8000 wsgi:app &
