#!/usr/bin/env bash

source $(dirname $0)/database-utils.sh

python directory/manage.py migrate && \
    if [ "$ENVIRONMENT" = "REVIEW-APP" ]; then create_database_super_user; fi

python directory/manage.py runserver 0.0.0.0:$PORT
