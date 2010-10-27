import os
from django.template import Library, Node, TemplateSyntaxError, Variable
from PIL import Image
from imageprocessor.presets import get_preset
from imageprocessor import settings, ImageProcessor
from imageprocessor.cache import ImageCache

register = Library()



class ThumbnailUrlNode(Node):
    def __init__(self, path, size, options):
        self.path = path
        self.size = size
        self.options = options
        self.thumbnails_cache = ImageCache(settings.THUMBNAIL_ROOT)

    def render(self, context):
        resolved_options = dict(zip([str(opt) for opt in self.options.keys()], [self.options[v].resolve(context) for v in self.options]))
        size = [int(z.resolve(context)) for z in self.size]
        path = str(self.path.resolve(context))
        if not path:
            raise TemplateSyntaxError('Provided image path is empty')
        if not os.path.isabs(path):
            path = os.path.join(settings.MEDIA_ROOT, path)
        try:
            processor = ImageProcessor()
            processor.add_filter(Image.Image.thumbnail, size, resample=Image.ANTIALIAS)
            return '%s%s' % (settings.THUMBNAIL_PREFIX, os.path.basename(
                self.thumbnails_cache.get_image_file(processor, path)))
        except (IOError, OSError), e:
            if not settings.FAIL_SILENTLY:
                raise e
            return ''


@register.tag(name='thumbnail_url')
def thumbnail_url(parser, token):
    bits = token.contents.split(' ')
    if len(bits) < 4:
        raise TemplateSyntaxError("'%s' takes at least two arguments"
                                  " (image path, width, height)" % bits[0])
    file, width, height = [parser.compile_filter(bit) for bit in bits[1:4]]
    options = {}

    if len(bits) > 4:
        bits = iter(bits[4:])
        for bit in bits:
            for arg in bit.split(","):
                if '=' in arg:
                    k, v = arg.split('=', 1)
                    k = k.strip()
                    options[k] = parser.compile_filter(v)
                elif arg:
                    raise TemplateSyntaxError("Unhandled parameter: %s" % bit)

    return ThumbnailUrlNode(file, (width, height), options)


class ImageFromPresetNode(Node):
    def __init__(self, path, preset_name, cast_as=None):
        self.path = Variable(path)
        self.preset_name = Variable(preset_name)
        self.cast_as = cast_as

    def render(self, context):
        try:
            preset_name = str(self.preset_name.resolve(context))
            path = str(self.path.resolve(context))
            preset = get_preset(preset_name)
            if os.path.isabs(path):
                source = path
            else:
                source = os.path.join(settings.MEDIA_ROOT, path)

            image = preset.get_image(source)

            url = u'%s%s%s/%s' % (settings.MEDIA_URL, settings.PRESETS_PREFIX,
                preset_name, os.path.basename(image.filename).decode('utf-8'))
                
            if self.cast_as:
                width, height = image.size
                context[self.cast_as] = {
                        'url': url,
                        'width': width,
                        'height': height,
                        'file': image.filename,
                        }
                return ''
            return url
        except (IOError, OSError), e:
            if not settings.FAIL_SILENTLY:
                raise e
            if self.cast_as:
                context[self.cast_as] = ''
            return ''

@register.tag
def image_from_preset(parser, token):
    bits = token.contents.split(' ')
    if len(bits) < 3:
        raise TemplateSyntaxError("'%s' takes at least two arguments"
                                  " (image path, preset name)" % bits[0])
    path, preset = bits[1:3]
    cast_as = None
    if len(bits)>4:
        if bits[3]!='as':
            raise TemplateSyntaxError(
                "Usage: '%s' imagepath preset_name [as value]" % bits[0])
        cast_as = bits[4]

    return ImageFromPresetNode(path, preset, cast_as)

