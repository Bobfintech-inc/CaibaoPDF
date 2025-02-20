#!/bin/sh

python -m celery -A project worker --loglevel=info
python -m celery -A project beat --loglevel=info
python manager.py runserver $SERVER_DOMAIN:$SERVER_PORT