echo
DATABASE_GR=sqlite3
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sh run_build_general.sh
sh run_server.sh