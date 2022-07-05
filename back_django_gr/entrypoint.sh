#!/bin/sh


echo "DATABASE : $DATABASE_GR"

#if [ "$DATABASE" = "postgres" ]
#then
#    echo "Waiting for postgres..."
#
#    while ! nc -z $SQL_HOST $SQL_PORT; do
#      sleep 0.1
#      echo "Check connection $SQL_HOST:$SQL_PORT"
#    done
#
#    echo "PostgreSQL started"
#fi

#x=1
#while [ $x -le 100 ];
#do
#  echo "---------"
#  x=$(( x+1 ))
#done

echo $(nc -v -z localhost 5430)
echo $(nc -v -z localhost 5432)
echo $(nc -v -z 127.0.0.1 5430)
echo $(nc -v -z 127.0.0.1 5432)

if ! nc -z localhost 5430
then
  echo "NOT connection on localhost:5430"
fi

if ! nc -z localhost 5432
then
  echo "NOT connection on localhost:5432"
fi

python manage.py flush --no-input
python manage.py migrate

exec "$@"
