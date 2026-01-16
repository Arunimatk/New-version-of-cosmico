#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
# python manage.py loaddata data.json # Removed to prevent overwriting manual data
python create_new_superuser.py
