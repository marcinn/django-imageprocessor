"""
@author: Marcin Nowak (marcin.j.nowak@gmail.com)

module provides ImageProcessor class for batch processing images
"""

from PIL import Image 
import os


class ImageProcessor(object):
    """
    modifies source image using filters queue
    rendering is executed after first call of render() or save() methods
    """

    def __init__(self, filters=None, output_dir=None, quality=75):
        """
        initializes processor for image file
        you can also set output quality (JPEG)
        """
        
        self.output_dir = output_dir
        self.rendered_image = None
        self.quality = quality 
        self.filters = filters or []

    def process(self, filename):
        """
        sets source image filename for processing
        """
        self.filename = filename
        self.rendered_image = None
        return self

    def add_filter(self, filter_instance, *args, **kwargs):
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



def filter_spec(filter_instance, *args, **kwargs):
    """
    helper for easy adding filters as init arg for processor
    """
    return (filter_instance, args, kwargs)
