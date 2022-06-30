echo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 ./scripts/generate_env.py
python3 manage.py makemigrations core
python3 manage.py migrate
python3 manage.py shell < ./scripts/generate_testDB.py
sh run_server.sh