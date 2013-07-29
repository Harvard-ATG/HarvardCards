# Google App Engine Settinsg
from harvardcards.settings.common import *

DATABASES = {
    'default': {
        'ENGINE': 'google.appengine.ext.django.backends.rdbms',
        'INSTANCE': 'dev-harvardcards:cloud2',
        'NAME': 'harvardcards',
    }
}