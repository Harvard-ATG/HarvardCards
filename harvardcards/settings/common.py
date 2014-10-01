# Common settings for all environments
import logging
import sys
from os import path
from glob import glob

# Django settings for harvardcards project.
DEBUG = True
TEMPLATE_DEBUG = DEBUG

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
ROOT_DIR = reduce(lambda l,r: path.dirname(l), range(3), path.realpath(__file__))

# Example: "/home/ubuntu/harvardcards/harvardcards"
PROJECT_ROOT = path.join(ROOT_DIR, 'harvardcards')

# Example: "/home/ubuntu/harvardcards/harvardcards/apps"
APPS_ROOT = path.join(PROJECT_ROOT, 'apps')

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = path.join(APPS_ROOT, 'flash', 'uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = 'static'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = [
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	path.join(PROJECT_ROOT, 'static'),
]

STATICFILES_DIRS.extend([ 
	f for f in glob(path.join(APPS_ROOT, '*', 'static')) if path.isdir(f)
])

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
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

TEMPLATE_DIRS = [
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    path.join(PROJECT_ROOT, 'templates'),
]

TEMPLATE_DIRS.extend([
    f for f in glob(path.join(APPS_ROOT, '*', 'templates')) if path.isdir(f)
])

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
)

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
    'harvardcards.apps.flash',
    #'harvardcards.apps.jasmine',
    'south',
]

FIXTURE_DIRS = (
    'harvardcards.apps.flash.fixtures'
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
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': path.join(ROOT_DIR, 'logs', 'debug.log'),
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': path.join(ROOT_DIR, 'logs', 'info.log'),
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': path.join(ROOT_DIR, 'logs', 'warning.log'),
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': path.join(ROOT_DIR, 'logs', 'error.log'),
        },
        'file': {
            'level': 'CRITICAL',
            'class': 'logging.FileHandler',
            'filename': path.join(ROOT_DIR, 'logs', 'critical.log'),
        },
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'harvardcards': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

if DEBUG:
    LOGGING['loggers']['harvardcards']['level'] = 'DEBUG'
    #LOGGING['loggers']['harvardcards']['handlers'] += ['console']

OPENID_CREATE_USERS = True
OPENID_UPDATE_DETAILS_FROM_SREG = True
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/logout/'
OPENID_SSO_SERVER_URL = 'https://www.google.com/accounts/o8/id'

