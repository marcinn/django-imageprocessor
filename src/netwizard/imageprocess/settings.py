import os
from django.conf import settings
MEDIA_ROOT = settings.MEDIA_ROOT

THUMBNAIL_PREFIX = getattr(settings, 'IMAGEPROCESS_THUMBNAIL_PREFIX', 'thumbs/')
THUMBNAIL_ROOT = getattr(settings, 'IMAGEPROCESS_THUMBNAIL_ROOT', os.path.join(settings.MEDIA_ROOT, 'thumbs'))

JPEG_QUALITY = getattr(settings, 'IMAGEPROCESS_JPEG_QUALITY', 75)

PRESETS_PREFIX = getattr(settings, 'IMAGEPROCESS_PRESETS_PREFIX', 'presets/')
PRESETS_ROOT = getattr(settings, 'IMAGEPROCESS_PRESETS_ROOT', os.path.join(settings.MEDIA_ROOT, 'presets'))
