import os
import os.path
import dj_database_url
import dotenv
from .base import *

dotenv.read_dotenv(os.path.join(ROOT_DIR, '.env'))

ALLOWED_HOSTS = ['localhost']

DEBUG = True
SECRET_KEY = '#5g0vp545jp644!hha1)fb7v1hd!*t#b@fv&amp;1(mrnt5)$q%w0g'
DATABASES = {
    'default': dj_database_url.config(default='postgres://flash:password@127.0.0.1:5432/flash')
}
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3', 
#        'NAME': path.join(ROOT_DIR, 'flash.db'),    
#        # The following settings are not used with sqlite3:
#        'USER': '',
#        'PASSWORD': '',
#        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
#        'PORT': '',                      # Set to empty string for default.
#    }
#}

MEDIA_STORE_BACKEND = os.environ.get("MEDIA_STORE_BACKEND", "file")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", None)
AWS_ACCESS_SECRET_KEY = os.environ.get("AWS_ACCESS_SECRET_KEY", None)
AWS_S3_BUCKET  = os.environ.get("AWS_S3_BUCKET", None)

LTI_OAUTH_CREDENTIALS = {"flashkey":"flashsecret"}
