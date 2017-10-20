#!/usr/bin/env bash
git pull
kill $(ps aux | grep 'final-project' | awk '{print $2}')
nohup gunicorn --certfile cert.pem --keyfile key.pem -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 -b 0.0.0.0:3040 wsgi:app &
