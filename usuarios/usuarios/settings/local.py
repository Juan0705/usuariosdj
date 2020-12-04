from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret('DB_NAME'),
        'USER': get_secret('USER'),
        'PASSWORD': get_secret('PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


STATIC_URL = '/static/'
# dentro de la carpeta static estan guardados los archivos estaticos (BOOTSTRAP, FOUNDATION, etc)
STATICFILES_DIRS = [BASE_DIR.child('static')]


MEDIA_URL = '/media/'
# dentro de la carpeta media estan guardados los archivos multimedia (imagenes, musica, etc)
MEDIA_ROOT = BASE_DIR.child('media')
