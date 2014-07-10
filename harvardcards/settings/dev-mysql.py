from harvardcards.settings.common import *

import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
		'OPTIONS': {
			'read_default_file': os.path.join(ROOT_DIR, 'config', 'my.cnf'),
		},
        #'NAME': 'flashdb',    # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        #'USER': 'flashuser',
        #'PASSWORD': 'flashpass',
        #'HOST': 'localhost',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        #'PORT': '3306',                      # Set to empty string for default.
    }
}

# Configuration for the django-debug-toolbar 
# (pip install django-debug-toolbar)
#
# Uncomment these lines to enable the toolbar
#MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')
#INSTALLED_APPS.append('debug_toolbar')
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': lambda x: True,
    'HIDE_DJANGO_SQL': False,
    'TAG': 'div',
    'ENABLE_STACKTRACES': True,
    #'HIDDEN_STACKTRACE_MODULES': ('gunicorn', 'newrelic'),
}
