#!/bin/sh

# we want to run migrations always before running the app on gunicorn server which is a WSGI HTTP servers for python that allows applications to run concurrently
flask db upgrade

exec gunicorn --bind 0.0.0.0:80 "app:create_app()"