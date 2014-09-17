from harvardcards.settings.common import *

DEBUG = True
SECRET_KEY = '#5g0vp545jp644!hha1)fb7v1hd!*t#b@fv&amp;1(mrnt5)$q%w0g'
LTI_OAUTH_CREDENTIALS = {"flashkey":"flashsecret"}

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

#########################################
# Configuration for the django-debug-toolbar 
#
#		pip install django-debug-toolbar
#
# Uncomment the MIDDLEWARE_CLASSES and INSTALLED_APPS lines
# to enable the django debug toolbar.
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': "%s.true" % __name__,
    'ENABLE_STACKTRACES': True,
}

#MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')
#INSTALLED_APPS.append('debug_toolbar')

def true(request):
	'''For the django debug toolbar callback. Returns true to enable it.'''
	return True
