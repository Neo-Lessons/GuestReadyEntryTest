from .general_settings import *

DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_grET',
        'USER': 'admin',
        'PASSWORD': 'root',
        'HOST': '0.0.0.0',
        'PORT': '5430',
    }
}