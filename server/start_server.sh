#!/bin/sh
set -e
FLASK_APP=app.app flask
PORT=${PORT:-5000}
exec gunicorn -b :${PORT} --access-logfile - --error-logfile - -k gevent -w 4 "app.app:create_app()"
