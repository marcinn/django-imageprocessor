""" 
@author Marcin Nowak (marcin.j.nowak@gmail.com)

This module provides extra-filters and filters registry
that provides easy access to filters and modifiers by name
"""

from PIL import Image 
from PIL import ImageEnhance
from PIL import ImageChops


class FiltersRegistry(object):
    def __init__(self):
        self.filters = {}

    def register(self, name, filter):
        if self.filters.has_key(name):
            raise KeyError('Filter "%s" is already registered')
        self.filters[name] = filter

    def unregister(self, name_or_instance):
        if isinstance(name_or_instance, str):
            self.filters.pop(name_or_instance)
        else:
            for name, filter in self.filters.items():
                if filter == name_or_instance:
                    self.filters.pop(name)

    def register_once(self, name, filter):
        try:
            return self.register(name, filter)
        except KeyError:
            pass

    def get(self, name):
        return self.filters[name]


# system-wide filters registry

library = FiltersRegistry()


# Common PIL filters


library.register('rotate',     Image.Image.rotate)       # use built-in func as rotate filter
library.register('thumbnail',  Image.Image.thumbnail)    # use built-in func as thumbnail filter

# PIL`s common enhance wrappers


def grayscale(image, *args, **kwargs):
    return ImageEnhance.Color(image).enhance(0)

library.register('grayscale', grayscale)


# PIL`s common channel operations

library.register('invert', ImageChops.invert)
library.register('multiply', ImageChops.multiply)
library.register('screen', ImageChops.screen)
library.register('add', ImageChops.add)
library.register('subtract', ImageChops.subtract)
library.register('blend', ImageChops.blend)
library.register('composite', ImageChops.composite)


# custom filters

def watermark(im, mark, position=('right','bottom',), opacity=1.0):
    """
    applies watermark onto image
    im - destination image PIL.Image instance
    mark - watermark image PIL.Image instance
    position - (xpos, ypos) tuple, where:
        xpos: left, right, center
        ypos: top, bottom, center 
    opacity - 0..1
    """
    layer = Image.new('RGBA', im.size, (0,0,0,0))

    _xpos = {'left': 0, 'right': im.size[0]-mark.size[0], 'center': (im.size[0]-mark.size[0])/2,}
    _ypos = {'top': 0, 'bottom': im.size[1]-mark.size[1], 'center': (im.size[1]-mark.size[1])/2,}
    
    try:
        x, y = _xpos[position[0]], _ypos[position[1]]
    except KeyError:
        raise RuntimeError('Invalid watermark position placement: %s' % str(position))

    layer.paste(mark, (x,y))
    return Image.composite(layer, im, layer)
       

library.register('watermark', watermark)
