#!/bin/sh

python manage.py collectstatic --no-input --clear
python manage.py migrate
python manage.py runserver 8000