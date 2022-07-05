from .general_settings import *
import os

DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # NEO: 04.07.22 18:15 (~006) [DOKERIZATION]
        # <CHANGE> <OLD>
        # 'NAME': 'db_grET',
        # 'USER': 'admin',
        # 'PASSWORD': 'root',
        # 'HOST': '127.0.0.1',
        # 'PORT': '5430',
        # </OLD> <NEW>
        'NAME': os.environ.get("SQL_DATABASE", 'db_grET'),
        'USER': os.environ.get("SQL_USER", 'admin'),
        'PASSWORD': os.environ.get("SQL_PASSWORD", 'root'),
        'HOST': os.environ.get("SQL_HOST", '127.0.0.1'),
        'PORT': os.environ.get("SQL_PORT", '5432'),
        # </NEW> </CHANGE>
    }
}