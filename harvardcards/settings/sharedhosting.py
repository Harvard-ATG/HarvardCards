# Shared hosting settings (sites.fas)
from harvardcards.settings.common import *
import os

DEBUG = False
ALLOWED_HOSTS = ['.fas.harvard.edu'] # Required when Debug=False
FORCE_SCRIPT_NAME = None
STATIC_URL = '/static/'

# Configuration specific to shared hosting PROD/DEV environments
# PRODUCTION
if os.environ.get('SERVER_NAME') == 'flashcards.fas.harvard.edu':
    FORCE_SCRIPT_NAME = '/'
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    DEBUG = False
# DEVELOPMENT
elif os.environ.get('SERVER_NAME') == 'sites.dev.fas.harvard.edu':
    FORCE_SCRIPT_NAME = '/~harvardcards/'
    STATIC_URL = '/~harvardcards/static/'
    MEDIA_URL = '/~harvardcards/media/'
    DEBUG = True

# Make sure to filter out "console" from handlers because it logs to STDOUT$                             
# which won't work since the app runs in CGI mode on shared hosting and this$                            
# will result in an HTTP 500 Internal Server Error.$                                                     
LOGGING['loggers']['harvardcards']['handlers'] = [h for h in LOGGING['loggers']['harvardcards']['handlers'] if h != 'console']

# Configuration common to both PROD/DEV 
CONFIG_DIR = os.path.join(ROOT_DIR, 'config')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'OPTIONS': {
            'read_default_file': os.path.join(CONFIG_DIR, 'my.cnf'),
        }
    }
}

# These are sensitive values that should be retrieved from separate configuration files.
# Note that these config files should *NEVER* be stored in version control.
SECRET_KEY = None
with open(os.path.join(CONFIG_DIR, 'django_secret.txt')) as f:
    SECRET_KEY = f.read().strip()

LTI_OAUTH_CREDENTIALS = {}
with open(os.path.join(CONFIG_DIR, 'lti_oauth_credentials.txt')) as f:
    oauth_key_and_secret = f.read().strip().split(':',2)
    LTI_OAUTH_CREDENTIALS = dict([tuple(oauth_key_and_secret)])
