#!/bin/bash
cd /focus_mate_back/focus_mate/
cd /focus_mate/

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:80  