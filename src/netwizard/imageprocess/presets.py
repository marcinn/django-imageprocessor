"""
Image presets module
author: Marcin Nowak (marcin.j.nowak@gmail.com)
"""

import os

class Preset(object):
    """
    Preset instance represents image rendering settings
    and optional output place
    """

    def __init__(self, image_class, filters=None, \
            output_dir=None, file_pattern=None, quality=None):
        """
        initializes preset with specified image class,
        filters set, quality, and output file settings
        """
        self.filters = filters
        self.image_class = image_class
        self.output_dir = output_dir
        self.file_pattern = file_pattern
        self.quality = quality

    def __repr__(self):
        return '[%s], %d filters, output=%s' % (self.image_class,
                len(self.filters), os.path.join(self.output_dir,
                    self.file_pattern))
            


def get_preset_image(filename, preset_name):
    """
    returns image instance created from file and
    prepared using preset, which is registered 
    by name
    """
    import settings
    preset = library.get(preset_name)
    image = preset.image_class(filename=filename, quality=preset.quality)
    for filter_instance, args, options in preset.filters:
        if isinstance(filter_instance, str):
            getattr(image, filter_instance)(*args, **options)
        else:
            image.process(filter_instance, *args, **options)
    filename, ext = os.path.splitext(os.path.split(image.filename)[1])
    pattern_args = {'filename': filename, 'ext': ext}

    outfilename = preset.file_pattern or '%(filename)s%(ext)s' 
    outfilename = outfilename % pattern_args
    outdir = preset.output_dir or (os.path.join(settings.PRESETS_ROOT, 
        preset_name))
    if not os.path.isdir(outdir):
        os.makedirs(outdir, 0777)
    image.preset_name = preset_name
    
    image.save(outfile=os.path.join(outdir, outfilename))
    return image



class Library(object):
    """
    Class that represents presets registry
    """
    def __init__(self):
        """
        initializes presets registry instance
        """
        self.presets = {}

    def register(self, name, preset):
        """
        register preset instance by name
        """
        if self.presets.has_key(name):
            raise KeyError('Preset with name "%s" already registered' % name)
        self.presets[name] = preset

    def register_once(self, name, preset):
        """
        Register preset instance by name.
        If preset is already registered,
        registration will be skipped without
        exception.
        """
        try:
            self.register(name, preset)
        except KeyError:
            pass

    def unregister(self, name):
        """
        Removes preset from registry
        """
        self.presets.pop(name)

    def get(self, name):
        """
        Access preset instance from registry
        by name
        """
        return self.presets[name]


# library represents default presets registry

library = Library()


