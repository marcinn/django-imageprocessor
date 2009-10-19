""" 
@author Marcin Nowak (marcin.j.nowak@gmail.com)

This module provides extra image filters
"""


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
       

def filter_spec(filter_instance, *args, **kwargs):
    """
    helper for easy adding filters as init arg for processor
    """
    return (filter_instance, args, kwargs)
