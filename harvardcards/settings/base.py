# Common settings for all environments
import logging
import sys
import os
from os import path

# Django settings for harvardcards project.
DEBUG = True

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

### SET PATH INFORMATION ###############################################
# Example: "/home/ubuntu/harvardcards"
ROOT_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = path.join(ROOT_DIR, 'uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = path.join(ROOT_DIR, 'http_static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = [
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	path.join(ROOT_DIR, 'static'),
]

TEMPLATES = [
	{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
			path.join(ROOT_DIR, 'templates'),
			path.join(ROOT_DIR, 'flash', 'templates'),
			path.join(ROOT_DIR, 'jasmine', 'templates'),
		],
		'OPTIONS': {
			'debug': True,
            'context_processors': [
                	"django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages"
            ],
			'loaders': [
			    'django.template.loaders.filesystem.Loader',
			    'django.template.loaders.app_directories.Loader',
				# 'django.template.loaders.eggs.Loader',
			]
		}
    }
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_auth_lti.middleware.LTIAuthMiddleware',
]

ROOT_URLCONF = 'harvardcards.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'harvardcards.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django_openid_auth',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'flash',
    #'jasmine'
]

FIXTURE_DIRS = (
    'flash.fixtures',
)

AUTHENTICATION_BACKENDS = (
    #'libs.auth.GoogleBackend',
    #'django_openid_auth.auth.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
    'django_auth_lti.backends.LTIAuthBackend',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False, # don't override default django logging config
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s %(user)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level' : 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'flash': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
