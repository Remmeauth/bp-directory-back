#!/usr/bin/env bash

python directory/manage.py migrate
python directory/manage.py runserver 0.0.0.0:$PORT
