""" Easy image processing library using PIL """

"""
example usage:

    img = CachedImage('/tmp/my_image.png').thumbnail([120,80]).grayscale().render()
    img.save('/tmp/processed_image.png')
    print img.filename  # get output filename
    print img   # string (raw) representation

    change cache dir:

    img = CachedImage('/tmp/my_image.png').thumbnail([120,80]).grayscale()
    img.cache_dir = '/tmp/cache/'
    print img.render().filename     # cached file path

"""



import Image as _Image
from PIL import Image as _pImage
import md5
import UserList
import os

# available filters

filters = {}

""" register a custom filter """
def register_filter(key, filter):
    filters[key] = filter


class ImageFilters(UserList.UserList):

    def mkhash(self):
        result = md5.new()
        for filter, args, kwargs in self:
            result.update(filter.__name__)
            result.update(str(args))
            result.update(str(kwargs))

        return result.hexdigest()


""" Base image class """
class Image(object):
    
    filters = ImageFilters()
    filename = None
    rendered_image = None

    def __init__(self,filename=None):
        self.load(filename)

    def load(self,file):
        self.filename = file
        self.filters = ImageFilters()
        return self

    def add_filter(self, name, *args, **kwargs):
       if filters.has_key(name):
           return self.process(filters[name], *args, **kwargs)
       raise AttributeError("Unknown filter %s." % name)

    def __getattr__(self, attr):
        def callable(*args, **kwargs):
            return self.add_filter(attr, *args, **kwargs)
        return callable

    def process(self, filter_instance, *args, **kwargs):
        self.rendered_image = None
        self.filters.append( (filter_instance, args, kwargs) )
        return self

    def render(self):
        if not self.rendered_image:
            if not self.filename:
                raise 'Image file not selected'
            img = _pImage.open(self.filename)
            for filter_instance, args, kwargs in self.filters:
                result = filter_instance(img, *args, **kwargs)
                # some filters returns a copy of an image, so check it
                # and replace image resource
                if isinstance(result, _pImage.Image):
                    img.im = result.im
            self.rendered_image = img
        return self

    def save(self, outfile=None):
        if not self.rendered_image:
            self.render()

        if not outfile:
            outfile = self.filename

        self.filename = outfile
        self.rendered_image.save(outfile, format=self.rendered_image.format)
        return self

    def __str__(self):
        self.render()
        return self.rendered_image.tostring()


CACHE_DIR = '/tmp/'

""" cached image class """
class CachedImage(Image):

    def __init__(self, *args, **kwargs):
        super(CachedImage, self).__init__(*args, **kwargs)
        self.cache_dir = CACHE_DIR
        self.cached = False

    def render(self):
        cache = os.path.join( self.cache_dir, str(md5.new(self.filename + str(os.path.getsize(self.filename)) + self.filters.mkhash() + self.filename).hexdigest()) )
        if os.path.exists(cache):
            self.cached = True
            self.filename = cache
            self.rendered_image = _pImage.open(self.filename)
            return self
        self.cached = False
        result = super(CachedImage,self).render()
        self.save(cache)
        return result
