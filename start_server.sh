#!/usr/bin/env bash
git pull
kill $(ps aux | grep 'final-project' | awk '{print $2}')
nohup gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8000 wsgi:app --worker-connections 5000 &
nohup gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8001 wsgi:app --worker-connections 5000 &
nohup gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8002 wsgi:app --worker-connections 5000 &
nohup gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8003 wsgi:app --worker-connections 5000 &
nohup gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8004 wsgi:app --worker-connections 5000 &
nohup gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8005 wsgi:app --worker-connections 5000 &
nohup gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8006 wsgi:app --worker-connections 5000 &
nohup gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8007 wsgi:app --worker-connections 5000 &
nohup gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8008 wsgi:app --worker-connections 5000 &
