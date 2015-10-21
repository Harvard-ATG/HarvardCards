from django import template
from django.template.defaultfilters import stringfilter
from django.conf import settings
from flash.media_store_service import get_s3_url, CONST_ORIGINAL, CONST_THUMB_LARGE, CONST_THUMB_SMALL

register = template.Library()

@register.filter
def as_media_url(value, arg):
    object_id = value
    object_category = arg
    item_path = "store/%s/%s" % (object_category, object_id)
    if settings.MEDIA_STORE_BACKEND == 's3':
        url = get_s3_url(item_path)
    else:
        url = settings.MEDIA_URL + item_path
    return url

@register.filter
@stringfilter
def as_original_media_url(value):
    return as_media_url(value, CONST_ORIGINAL)

@register.filter
@stringfilter
def as_large_media_url(value):
    return as_media_url(value, CONST_THUMB_LARGE)

@register.filter
@stringfilter
def as_small_media_url(value):
    return as_media_url(value, CONST_THUMB_SMALL)