import os
import os.path
import json
import dj_database_url
import dotenv
from .base import *

dotenv.read_dotenv(os.path.join(ROOT_DIR, '.env'))

ALLOWED_HOSTS = ['*']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

DATABASES = {
    'default': dj_database_url.config(default='postgres://flash:password@127.0.0.1:5432/flash')
}

STATIC_ROOT = 'staticfiles'

MEDIA_STORE_BACKEND = os.environ.get("MEDIA_STORE_BACKEND")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", None)
AWS_ACCESS_SECRET_KEY = os.environ.get("AWS_ACCESS_SECRET_KEY", None)
AWS_S3_BUCKET  = os.environ.get("AWS_S3_BUCKET", None)

LIT_OAUTH_CREDENTIALS = {}
if os.environ.get('LTI_OAUTH_CREDENTIALS', None):
    LTI_OAUTH_CREDENTIALS = json.loads(os.environ.get('LTI_OAUTH_CREDENTIALS'))
