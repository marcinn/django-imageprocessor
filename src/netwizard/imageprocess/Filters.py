""" custom filters and wrappers """

import Image 

# Common PIL filters

from PIL import Image as _pImage

Image.register_filter('rotate',     _pImage.Image.rotate)       # use built-in func as rotate filter
Image.register_filter('thumbnail',  _pImage.Image.thumbnail)    # use built-in func as thumbnail filter

# PIL`s common enhance wrappers

from PIL import ImageEnhance

def grayscale(image, *args, **kwargs):
    return ImageEnhance.Color(image).enhance(0)

Image.register_filter('grayscale', grayscale)


# PIL`s common channel operations

from PIL import ImageChops

Image.register_filter('invert', ImageChops.invert)
Image.register_filter('multiply', ImageChops.multiply)
Image.register_filter('screen', ImageChops.screen)
Image.register_filter('add', ImageChops.add)
Image.register_filter('subtract', ImageChops.subtract)
Image.register_filter('blend', ImageChops.blend)
Image.register_filter('composite', ImageChops.composite)


# custom filters

def watermark(image, watermark, position=('right', 'bottom'), **kwargs):
    pass
