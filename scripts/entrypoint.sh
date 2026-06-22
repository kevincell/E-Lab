#!/bin/sh
set -e

python manage.py wait_for_db
exec "$@"
