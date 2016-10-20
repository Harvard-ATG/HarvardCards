from django import template
from django.conf import settings
import datetime

register = template.Library()

@register.simple_tag
def requirejs_version():
  version_str = ''
  if settings.JS_BUILD_VERSION:
    version_str = settings.JS_BUILD_VERSION
  elif settings.DEBUG:
      version_str = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
  return version_str