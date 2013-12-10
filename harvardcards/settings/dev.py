# Google App Engine Settinsg
from harvardcards.settings.common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'flash.db',    # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Configuration for the django-debug-toolbar 
# (pip install django-debug-toolbar)
MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')
INSTALLED_APPS.append('debug_toolbar')
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': True,
    'SHOW_TOOLBAR_CALLBACK': lambda x: True,
    'HIDE_DJANGO_SQL': False,
    'TAG': 'div',
    'ENABLE_STACKTRACES': True,
    'HIDDEN_STACKTRACE_MODULES': ('gunicorn', 'newrelic'),
}
