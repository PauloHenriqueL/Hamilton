#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate auth
python manage.py migrate admin
python manage.py migrate contenttypes
python manage.py migrate sessions