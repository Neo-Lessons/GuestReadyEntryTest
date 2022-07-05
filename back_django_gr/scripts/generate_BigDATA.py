# (~004) Big data factory
from modules.core.factory import bigDATA

bigDATA.BigDataSets().generateBigData(10000)

# Debug execure string
# from modules.core.factory import bigDATA; bigDATA.BigDataSets().generateBigData(100000)
# shell -c "print('start');exec(open('scripts/generate_BigDATA.py').read())"
# manage.py shell -c "print('start');from scripts import generate_BigDATA"
