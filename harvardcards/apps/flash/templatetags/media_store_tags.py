from django import template
from django.conf import settings

register = template.Library()

def as_media_url(value, arg):
    object_id = value
    object_path = arg
    if settings.MEDIA_STORE_BACKEND == 's3':
        url = "http://s3.amazonaws.com/%s/%s/%s" % (settings.AWS_S3_BUCKET, object_path, object_id)
    else:
        url = settings.MEDIA_URL
        url += "%s/%s" % (object_path, object_id)
    return url

register.filter("as_media_url", as_media_url)