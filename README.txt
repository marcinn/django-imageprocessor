= django-imageprocessor =

Provides a simple way to batch converting images with cache and presets support.

== Common use cases ==

  - automatic generating thumbnails
  - automatic generating static, but processed (scaled, watermarked, etc) pictures

== Features ==

  - Cache: reduces processing time
  - Templates: two powerful template tags
  - API: simple, compatible with PIL`s chops, filters, transforms
  - No database needed


== Usage ==


=== Thumbnailer ===

In your templates put:

{{{

    {% load imageprocess %}
    <img src="{{ MEDIA_URL }}{% thumbnail_url your_model.image 120 80 %}" />

}}}

This will scale your_model.image to 120x80 size, preserving aspect ratio, resampled with Antialias,
and cached.


=== Watermarking ===

This app does NOT support watermarking directly. You must use external application.
django-imageprocessor is compatible with django-watermark (http://code.google.com/p/django-watermark/)

So, to configure your watermarking batch processor simply put these lines in your settings.py:

{{{

from watermarker.utils import watermark
from imageprocessor.presets import create_preset
from imageprocessor import ImageProcessor

my_watermark_image = Image.open(os.path.join(MEDIA_ROOT, 'images', 'watermark.png'))

create_preset('watermarked', 
    ImageProcessor(quality=90).add_filter(watermark, my_watermark_image, 'br'))

}}}

In your templates put:

{{{

    {% load imageprocess %}
    <img src="{{ MEDIA_URL }}{% image_from_preset your_model.image "watermarked" %}" />

}}}

If you want to scale your source image, put another filter before watermarking (settings.py):

{{{
    from PIL import Image
    add_filter(Image.Image.thumbnail, (800, 600), resample=Image.ANTIALIAS).
}}}


Full example of settings.py:

{{{

from PIL import Image
from watermarker.utils import watermark
from imageprocessor.presets import create_preset
from imageprocessor import ImageProcessor

my_watermark_image = Image.open(os.path.join(MEDIA_ROOT, 'images', 'watermark.png'))

create_preset('watermarked', ImageProcessor(quality=90).
        add_filter(Image.Image.thumbnail, (800, 600), resample=Image.ANTIALIAS).
        add_filter(watermark, my_watermark_image, 'br'))

}}}


== API ==

=== Processors ===

@todo

=== Presets ===

@todo

