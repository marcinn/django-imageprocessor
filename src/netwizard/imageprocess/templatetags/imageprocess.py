from netwizard.imageprocess import helpers 
from django.template import Library, Node, TemplateSyntaxError
from django.conf import settings
import os

register = Library()

class ThumbnailUrlNode(Node):
    def __init__(self, path, size, options):
        self.path = path
        self.size = size
        self.options = options

    def render(self, context):
        resolved_options = dict(zip([str(opt) for opt in self.options.keys()], [self.options[v].resolve(context) for v in self.options]))
        size = [int(z.resolve(context)) for z in self.size]
        path = str(self.path.resolve(context))
        if not path:
            raise TemplateSyntaxError('Provided image path is empty')
        if not os.path.isabs(path):
            path = os.path.join(settings.MEDIA_ROOT, path)
        try:
            return helpers.thumbnail_url(path, size, **resolved_options)
        except IOError:
            return None


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

