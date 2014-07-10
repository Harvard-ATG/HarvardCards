# Shared hosting settings (sites.fas)
from harvardcards.settings.common import *
import os

#STATIC_URL = '/~harvardcards/static/'

#FORCE_SCRIPT_NAME = '/~harvardcards/index.py'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
		'OPTIONS': {
			'read_default_file': os.path.join(ROOT_DIR, 'config', 'my.cnf'),
		},
        #'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        #'NAME': os.path.join(ROOT_DIR, 'flash.db'),
        # The following settings are not used with sqlite3:
        #'USER': '',
        #'PASSWORD': '',
        #'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        #'PORT': '',                      # Set to empty string for default.
    }
}
