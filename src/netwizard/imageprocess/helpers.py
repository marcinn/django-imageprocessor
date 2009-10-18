""" helpers for image processing """

from Image import CachedImage
from PIL import Image as PILImage
from presets import library, get_preset_image
import settings
import os

def register_thumbnail_pre_filter(name, *args, **kwargs):
    settings.THUMBNAIL_PRE_FILTERS.append((name, args, kwargs))

def register_thumbnail_post_filter(name, *args, **kwargs):
    settings.THUMBNAIL_POST_FILTERS.append((name, args, kwargs))

def thumbnail_url(file, size, filters=None, **opts):
    thumb = CachedImage(file, **opts).thumbnail(size, resample=PILImage.ANTIALIAS)
    thumb.cache_dir = settings.THUMBNAIL_CACHE_PATH
    filters = settings.THUMBNAIL_PRE_FILTERS + (filters or []) + settings.THUMBNAIL_POST_FILTERS
    for (filter_name, args, kwargs) in filters:
        if not kwargs:
            kwargs = {}
        getattr(thumb, filter_name)(*args, **kwargs)
    return u'%s%s' % (
            settings.THUMBNAIL_CACHE_PREFIX, 
            os.path.basename(thumb.save().filename)
            )

def url_from_preset(file, preset_name):
    image = get_preset_image(file, preset_name)
    return u'%s/%s/%s' % (settings.PRESETS_PREFIX, image.preset_name, 
            os.path.basename(image.filename))

