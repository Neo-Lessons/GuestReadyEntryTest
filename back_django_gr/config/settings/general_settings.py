from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# NEO: 02.07.22 22:59 (~001) [separation of settings]
# <CHANGE> <OLD>
# BASE_DIR = Path(__file__).resolve().parent.parent
# </OLD> <NEW>
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# </NEW> </CHANGE>


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# NEO: 03.07.22 00:11 (~001) [separation of settings]
# <CHANGE> <OLD>
# DEBUG = True
#
# ALLOWED_HOSTS = ['*']
# </OLD> </CHANGE>

#############################################################################
# Application definition
#############################################################################
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]
LOCAL_MODULE_APPS = [
    'modules.core.apps.CoreConfig',
    'modules.front_django',
    'modules.api_v1',
]
EXTERNAL_APPS = [
    'rest_framework',
    # NEO: 03.07.22 17:45 (~003) [APPEND API]
    # <NEW>
    'corsheaders',
    # </NEW> </CHANGE>
]
INSTALLED_APPS = DJANGO_APPS + LOCAL_MODULE_APPS + EXTERNAL_APPS
#############################################################################


MIDDLEWARE_DJANGO = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# NEO: 03.07.22 17:48 [Refactoring]
# <NEW>
MIDDLEWARE_LOCAL = [

]

MIDDLEWARE_EXTERNAL = [
    # NEO: 03.07.22 17:47 (~003) [APPEND API]
    # <NEW>
    'corsheaders.middleware.CorsMiddleware',
    # </NEW> </CHANGE>
]
# </NEW> </CHANGE>

MIDDLEWARE = MIDDLEWARE_DJANGO + MIDDLEWARE_LOCAL + MIDDLEWARE_EXTERNAL

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['src/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# NEO: 03.07.22 00:09 (~001) [separation of settings]
# <CHANGE> <OLD>
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
# </OLD>


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'src/static/'

STATICFILES_DIRS = [ BASE_DIR / "src/static"]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# NEO: 03.07.22 17:46 (~003) [APPEND API]
# <NEW>
CORS_ORIGIN_ALLOW_ALL=True
# </NEW> </CHANGE>
