#Generate environment
echo "!!!!!!!!!!!!!!!!!!!! Runing env generaton"
if [ "$DATABASE" = "postgres" ]
then
  echo "!!!!!!!!!!!!!!!!!!!! Run postgres env generaton"
  python3 ./scripts/generate_env_postgres.py
else
  echo "!!!!!!!!!!!!!!!!!!!! Run sqlite3 env generaton"
  python3 ./scripts/generate_env_sqlite3.py
fi

python3 manage.py makemigrations core
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py shell < ./scripts/generate_testDB.py