#!/usr/bin/env bash

CREATE_SUPER_USER_SCRIPT="
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('directory@gmail.com', 'directory-1337')
"

function create_database_super_user() {
  printf "$CREATE_SUPER_USER_SCRIPT" | python directory/manage.py shell
}
