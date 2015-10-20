from .base import *
from .secure import SECURE_SETTINGS

ALLOWED_HOSTS = ['.harvard.edu', 'localhost']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': SECURE_SETTINGS.get('db_default_name', 'harvardcards'),
        'USER': SECURE_SETTINGS.get('db_default_user', 'harvardcards'),
        'PASSWORD': SECURE_SETTINGS.get('db_default_password'),
        'HOST': SECURE_SETTINGS.get('db_default_host', '127.0.0.1'),
        'PORT': SECURE_SETTINGS.get('db_default_port', 5432),
    } 
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

REDIS_HOST = SECURE_SETTINGS.get('redis_host', '127.0.0.1')
REDIS_PORT = SECURE_SETTINGS.get('redis_port', 6379)

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': "%s:%s" % (REDIS_HOST, REDIS_PORT),
        'KEY_PREFIX': 'canvas_syllabus_export', # Provide a unique value for shared cache
        'TIMEOUT': SECURE_SETTINGS.get('cache_timeout_in_secs', 60 * 20),
    },
}

MEDIA_STORE_BACKEND = 's3'
AWS_ACCESS_KEY_ID = SECURE_SETTINGS.get('aws_key')
AWS_ACCESSS_SECRET_KEY = SECURE_SETTINGS.get('aws_secret')
AWS_S3_BUCKET = SECURE_SETTINGS.get('s3_bucket')

LTI_OAUTH_CREDENTIALS = SECURE_SETTINGS.get('lti_oauth_credentials', {})
