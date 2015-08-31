import dj_database_url
import os
import json
from harvardcards.settings.common import *

ALLOWED_HOSTS = ['*']

DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
LTI_OAUTH_CREDENTIALS = json.loads(os.environ.get('LTI_OAUTH_CREDENTIALS'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',    # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}
DATABASES['default'] =  dj_database_url.config()

#########################################
# Configuration for the django-debug-toolbar
#
#		pip install django-debug-toolbar
#
# Uncomment the MIDDLEWARE_CLASSES and INSTALLED_APPS lines
# to enable the django debug toolbar.
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    'ENABLE_STACKTRACES': True,
}

#MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')
#INSTALLED_APPS.append('debug_toolbar')

def true(request):
	'''For the django debug toolbar callback. Returns true to enable it.'''
	return True
