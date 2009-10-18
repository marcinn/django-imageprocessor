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
    layer = _pImage.new('RGBA', im.size, (0,0,0,0))

    _xpos = {'left': 0, 'right': im.size[0]-mark.size[0], 'center': (im.size[0]-mark.size[0])/2,}
    _ypos = {'top': 0, 'bottom': im.size[1]-mark.size[1], 'center': (im.size[1]-mark.size[1])/2,}
    
    try:
        x, y = _xpos[position[0]], _ypos[position[1]]
    except KeyError:
        raise RuntimeError('Invalid watermark position placement: %s' % str(position))

    layer.paste(mark, (x,y))
    return _pImage.composite(layer, im, layer)
       

Image.register_filter('watermark', watermark)
