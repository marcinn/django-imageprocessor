import os
from django.conf import settings

THUMBNAIL_CACHE_PREFIX = getattr(settings, 'THUMBNAIL_CACHE_PREFIX', 'thumbs/')
THUMBNAIL_CACHE_PATH = getattr(
        settings, 
        'THUMBNAIL_CACHE_PATH', 
        os.path.join(settings.MEDIA_ROOT, THUMBNAIL_CACHE_PREFIX))

THUMBNAIL_PRE_FILTERS = getattr(settings, 'THUMBNAIL_PRE_FILTERS', [])
THUMBNAIL_POST_FILTERS = getattr(settings, 'THUMBNAIL_POST_FILTERS', [])

JPEG_QUALITY = getattr(settings, 'IMAGEPROCESS_JPEG_QUALITY', 75)

PRESETS_ROOT = getattr(settings, 'IMAGEPROCESS_PRESETS_ROOT', os.path.join(settings.MEDIA_ROOT, 'presets'))
PRESETS_PREFIX = getattr(settings, 'IMAGEPROCESS_PRESETS_PREFIX', 'presets')

