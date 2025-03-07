#!/bin/sh


nohup env $(cat .env) python manage.py ocr_daemon > ocr_daemon.log 2>&1 &

nohup env $(cat .env) python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 & 
