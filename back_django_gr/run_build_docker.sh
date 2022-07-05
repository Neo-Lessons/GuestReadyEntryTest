#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      echo "Not connected $SQL_HOST $SQL_PORT"
      sleep 1
    done

    echo "PostgreSQL started"
fi

echo "!!!!!!!!!!!!!!!!!!!!!!!"
sh run_build_general.sh

exec "$@"