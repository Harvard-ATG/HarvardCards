# Shared hosting settings (sites.fas)
from harvardcards.settings.common import *
import os

DEBUG = False
FORCE_SCRIPT_NAME = None
STATIC_URL = '/static/'

# Configuration specific to shared hosting PROD/DEV environments
# PRODUCTION
if os.environ.get('SERVER_NAME') == 'flashcards.fas.harvard.edu':
    FORCE_SCRIPT_NAME = '/'
    STATIC_URL = '/static/'
	DEBUG = False
# DEVELOPMENT
elif os.environ.get('SERVER_NAME') == 'sites.dev.fas.harvard.edu':
    FORCE_SCRIPT_NAME = '/~harvardcards/'
    STATIC_URL = '/~harvardcards/static/'
	DEBUG = True

# Configuration common to both PROD/DEV 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'OPTIONS': {
            'read_default_file': os.path.join(ROOT_DIR, 'config', 'my.cnf'),
        }
    }
}

# These values should be retrieved from the environment for security reasons
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
LTI_OAUTH_CREDENTIALS = dict([tuple(os.environ.get('LTI_OAUTH_CREDENTIALS').split(':',2))])
