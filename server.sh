#!/bin/bash
cd /with_ance/with_ance_app/
cat .env
cd ./with_ance/
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:80  