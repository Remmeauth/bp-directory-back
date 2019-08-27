#!/usr/bin/env bash

CREATE_SUPER_USER_SCRIPT="
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('directory@gmail.com', 'directory', 'directory-1337')
"

function create_database_super_user() {
  printf "$CREATE_SUPER_USER_SCRIPT" | python directory/manage.py shell
}

function create_database_fixtures() {
  declare -a arr_fixtures=(
    "directory/user/fixtures/user.json"
    "directory/block_producer/fixtures/block_producer.json"
    "directory/services/fixtures/password_recovery_state.json"
  )

  for fixture in "${arr_fixtures[@]}"
  do
    python directory/manage.py loaddata $fixture
  done
}
