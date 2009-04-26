from netwizard.imageprocess import helpers 
from django.template import Library, Node
from django.conf import settings
import os

register = Library()

@register.simple_tag
def thumbnail_url(file, width, height):
    file = str(file)
    if not os.path.isabs(file):
        file = os.path.join(settings.MEDIA_ROOT, file)
    return helpers.thumbnail_url(file, (int(width),int(height)))
