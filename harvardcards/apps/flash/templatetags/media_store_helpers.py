from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='as_media_url')
def as_media_url(value, arg):
    object_id = value
    object_path = arg
    if settings.MEDIA_STORE_BACKEND == 's3':
        url = "http//s3.amazonaws.com/%s/%s/%s" % (settings.AWS_S3_BUCKET, object_path, object_id)
    else:
        url = settings.MEDIA_URL + "%s/%s" % (object_path, object_id)
    return url
