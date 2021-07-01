#!/bin/sh

/usr/local/bin/python3 manage.py init_database
/usr/local/bin/python3 -m gunicorn -b 0.0.0.0:5000 manage:app
