#!/usr/bin/env bash

POSTGRES_CONNECTIONS_TIMEOUT_MAX_LIMIT=20
CURRENT_POSTGRES_CONNECTIONS_ATTEMPTS=0
CREATE_SUPER_USER_SCRIPT="
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('directory@gmail.com', 'directory-1337', first_name='Admin', last_name='Directory')
"

function wait_until_postgres_is_started() {
  while true; do

    if (( $CURRENT_POSTGRES_CONNECTIONS_ATTEMPTS > $POSTGRES_CONNECTIONS_TIMEOUT_MAX_LIMIT )); then
      echo "Connection to PostgreSQL timed out or container still isn't running for 20 seconds!"
      exit 1
    fi

    CURRENT_POSTGRES_CONNECTIONS_ATTEMPTS=$(($CURRENT_POSTGRES_CONNECTIONS_ATTEMPTS + 1))
    if [ -z "$(pg_isready -h postgres -p 5432 | grep accepting)" ]; then
      sleep 1s
      continue

    else
      break
    fi

  done
}

function create_database_super_user() {
  printf "$CREATE_SUPER_USER_SCRIPT" | python directory/manage.py shell
}

function create_database_fixtures() {
  declare -a arr_fixtures=(
    "directory/user/fixtures/user.json"
    "directory/user/fixtures/profile.json"
    "directory/block_producer/fixtures/block_producer.json"
    "directory/block_producer/fixtures/block_producer_like.json"
    "directory/services/fixtures/password_recovery_state.json"
  )

  for fixture in "${arr_fixtures[@]}"
  do
    python directory/manage.py loaddata $fixture
  done
}
