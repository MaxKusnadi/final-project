#!/usr/bin/env bash
git pull
kill $(ps aux | grep 'final-project' | awk '{print $2}')
nohup gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8000 wsgi:app &
nohup gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8001 wsgi:app &
nohup gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8002 wsgi:app &
nohup gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8003 wsgi:app &
nohup gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8004 wsgi:app &
