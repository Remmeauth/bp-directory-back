#!/usr/bin/env bash

source $(dirname $0)/database-utils.sh

wait_until_postgres_is_started && \
    python directory/manage.py migrate

python directory/manage.py runserver 0.0.0.0:8000
