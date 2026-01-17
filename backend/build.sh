#!/usr/bin/env bash
# exit on error
set -o errexit
# Rebuild trigger for verification

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py loaddata data.json
python add_perfumes.py
python add_nail_polish.py
python create_new_superuser.py
python restore_backup.py
