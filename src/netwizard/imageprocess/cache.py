"""
caching layer for processors
"""
import hashlib
from PIL import Image
import os

def make_filters_hash(filters):
    result = hashlib.md5()
    for filter, args, kwargs in filters:
        result.update(filter.__name__)
        result.update(str(args))
        result.update(str(kwargs))
    return result.hexdigest()

class ImageCache(object):
    def __init__(self, cache_dir):
        self.cache_dir = cache_dir

    def get_image(self, processor, source, cache=None):
        cache = cache or self._get_cache_filename(processor, source)
        cache_path = os.path.join(self.cache_dir, cache)
        if os.path.exists(cache_path):
            return Image.open(cache_path)
        return processor.process(source).save(cache_path).rendered_image
        
    def get_image_file(self, processor, source, cache=None):
        cache = cache or self._get_cache_filename(processor, source)
        cache_path = os.path.join(self.cache_dir, cache)
        if not os.path.exists(cache_path):
            processor.process(source).save(cache_path)
        return cache_path
        
    def _get_cache_filename(self, processor, source):
        # make unique md5 hash from source file properties
        # and processor filters
        return '%s%s' % (str(hashlib.md5(str(processor.quality) + source\
                + str(os.path.getsize(source)) \
                + make_filters_hash(processor.filters) \
                + source).hexdigest()), os.path.splitext(source)[1])

        
