"""
@author: Marcin Nowak (marcin.j.nowak@gmail.com)

caching layer for processed images
"""

import hashlib
from PIL import Image
import os


def source_changed(source, cache):
    """
    returns True if source was changed (cache revalidation is needed)
    """
    return os.path.getmtime(source)>os.path.getmtime(cache)


def make_filters_hash(filters):
    """
    compute filters hash
    """
    result = hashlib.md5()
    for filter, args, kwargs in filters:
        result.update(filter.__name__)
        result.update(str(args))
        result.update(str(kwargs))
    return result.hexdigest()


class ImageCache(object):
    """
    provides access to cached images
    """

    def __init__(self, cache_dir):
        self.cache_dir = cache_dir
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    def get_image(self, processor, source, cache=None):
        """
        returns CachedImage retrieved from cache or None
        """
        cache = cache or self._get_cache_filename(processor, source)
        cache_path = os.path.join(self.cache_dir, cache)
        if os.path.exists(cache_path):
            return CachedImage(cache_path)
        
    def get_image_file(self, processor, source, cache=None):
        """
        returns processed PIL Image file path retrieved from cache 
        or generated using processor
        @deprecated
        @todo: needs refactoring
        """
        cache = cache or self._get_cache_filename(processor, source)
        cache_path = os.path.join(self.cache_dir, cache)
        if not os.path.exists(cache_path) or source_changed(source, cache):
            processor.process(source).save(cache_path)
        return cache_path
        
    def _get_cache_filename(self, processor, source):
        """
        make md5 hash filename from source file properties
        and processor filters
        """
        return '%s%s' % (str(hashlib.md5(str(processor.quality) + source\
                + str(os.path.getsize(source)) \
                + make_filters_hash(processor.filters) \
                + source).hexdigest()), os.path.splitext(source)[1])


class CachedImage(object):
    def __init__(self, filename):
        self.filename = filename
        self._image = None
    
    def __getattr__(self, k):
        if not self._image:
            self._image = Image.open(self.filename)
        return getattr(self._image, k)

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

