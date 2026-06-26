#!/bin/sh
set -e

python manage.py wait_for_db

mkdir -p /var/elab-sandbox
python manage.py check --deploy --fail-level ERROR

exec "$@"
