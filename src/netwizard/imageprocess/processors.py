""" Easy image processing library using PIL """

"""
example usage:

    img = CachedImageProcessor('/tmp/my_image.png').thumbnail([120,80]).grayscale().render()
    img.save('/tmp/processed_image.png')
    print img.filename  # get output filename
    print img   # string (raw) representation

    change cache dir:

    img = CachedImageProcessor('/tmp/my_image.png').thumbnail([120,80]).grayscale()
    img.cache_dir = '/tmp/cache/'
    print img.render().filename     # cached file path

"""

from PIL import Image 
from filters import library
import hashlib
import os

def make_filters_hash(filters):
    result = hashlib.md5()
    for filter, args, kwargs in filters:
        result.update(filter.__name__)
        result.update(str(args))
        result.update(str(kwargs))
    return result.hexdigest()

class ImageProcessor(object):
    """
    modifies source image using filters queue
    rendering is executed after first call of render() or save() methods
    """

    def __init__(self, filename, output_dir=None, quality=75, filters_registry=None):
        """
        initializes processor for image file
        you can also set output quality (JPEG) and custom filters registry
        """
        
        self.output_dir = output_dir
        self.open(filename)
        self.quality = quality 
        self.filters_registry = filters_registry or library

    def open(self, filename):
        """
        sets source image filename
        clears processor state
        """
        self.filename = filename
        self.filters = []
        return self

    def __getattr__(self, attr):
        """
        wrapper for easy accessing filters from registry used
        with this processor instance
        """
        def callable(*args, **kwargs):
            try:
                return self.process(
                        self.filters_registry.get(attr), *args, **kwargs)
            except KeyError:
                raise AttributeError("Unknown filter %s." % attr)
        return callable

    def process(self, filter_instance, *args, **kwargs):
        """
        adds filter with paramters to filters queue
        """
        self.rendered_image = None
        self.filters.append( (filter_instance, args, kwargs) )
        return self

    def render(self):
        """
        applies filters from queue on source image
        automatically loads resource if image is not yet loaded
        """

        if not self.rendered_image:
            if not self.filename:
                raise 'Image file not selected'
            img = Image.open(self.filename)
            self.transparency = img.info.get('transparency', None)
            for filter_instance, args, kwargs in self.filters:
                result = filter_instance(img, *args, **kwargs)
                # some filters returns a copy of an image, so check it
                # and replace image resource
                if isinstance(result, Image.Image):
                    img.im = result.im
            self.rendered_image = img
        return self

    def save(self, outfile=None):
        """
        saves rendered image to outfile or source file
        or to output_dir with original filename, if output dir was set

        calls render() if needed
        """

        if not self.rendered_image:
            self.render()

        if not outfile:
            if self.output_dir:
                outfile = os.path.join(self.output_dir, os.path.basename(self.filename))
            else:
                outfile = self.filename

        self.filename = outfile 
        kwargs = {
                'format':self.rendered_image.format,
                }

        if self.transparency:
            kwargs['transparency']=self.transparency
        if self.rendered_image.format == 'JPEG':
            kwargs['quality'] = self.quality 

        self.rendered_image.save(outfile, **kwargs)
        return self

    def __str__(self):
        self.render()
        return self.rendered_image.tostring()


class CachedImageProcessor(ImageProcessor):
    """
    Same as ImageProcessor, but using cache.

    This processor can check cache for already rendered image
    and returns destination image without processing.
    """

    def __init__(self, *args, **kwargs):
        """
        initializes cached processor
        you can specify cache_dir 
        """
        super(CachedImageProcessor, self).__init__(*args, **kwargs)
        self.cached = False
        self.cache_file = None # output filename

    def save(self, outfile=None):
        """
        saves rendered image if not cached or outfile is provided
        """
        autocache_file = self._get_cache_file()
        outfile = outfile or autocache_file
        self.cache_file = outfile
        if not self.rendered_image:
            self.render()
        if (self.cached and autocache_file != outfile) or not self.cached:
            return super(CachedImageProcessor, self).save(outfile=outfile)
        self.filename = self.cache_file
        return self

    def _get_cache_file(self):
        """
        automatically generates cache filename
        """
        filename = str(hashlib.md5(str(self.quality) + self.filename + str(os.path.getsize(self.filename)) + make_filters_hash(self.filters) + self.filename).hexdigest())
        filename += os.path.splitext(self.filename)[1]
        return os.path.join(self.output_dir or os.path.dirname(self.filename), filename)

    def render(self):
        """
        applies filters to image if needed
        but if cached it only opens already rendered (cached) image
        """
        if not self.cache_file:
            """
            rendering cached image firstly checks for already generated image
            but if output filename is not set, render should fail
            """
            raise RuntimeError('Cache filename not set. Cannot render.')

        if os.path.exists(self.cache_file):
            self.cached = True
            self.rendered_image = Image.open(self.cache_file)
            return self

        self.cached = False
        return super(CachedImageProcessor,self).render()
