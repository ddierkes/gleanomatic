#! /bin/bash
export FLASK_APP=app/main.py
export FLASK_DEBUG=1

/usr/local/bin/flask run --host=0.0.0.0 --port=81
