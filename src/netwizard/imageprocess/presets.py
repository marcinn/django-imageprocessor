"""
Image presets module
author: Marcin Nowak (marcin.j.nowak@gmail.com)
"""

import os

class Preset(object):
    def __init__(self, image_class, filters=None, output_dir=None, file_pattern=None, quality=None):
        self.filters = filters
        self.image_class = image_class
        self.output_dir = output_dir
        self.file_pattern = file_pattern
        self.quality = quality


def get_preset_image(file, preset_name):
    import settings
    preset = library.get(preset_name)
    image = preset.image_class(filename=file, quality=preset.quality)
    for filter, args, options in preset.filters:
        if isinstance(filter, str):
            getattr(image, filter)(*args, **options)
        else:
            image.process(filter, *args, **options)
    filename, ext = os.path.splitext(os.path.split(image.filename)[1])
    pattern_args = {'filename': filename, 'ext': ext,}

    outfilename = preset.file_pattern or '%(filename)s%(ext)s' 
    outfilename = outfilename % pattern_args
    outdir = preset.output_dir or (os.path.join(settings.PRESETS_ROOT, preset_name))
    if not os.path.isdir(outdir):
        os.makedirs(outdir, 0777)
    image.preset_name = preset_name
    
    image.save(outfile=os.path.join(outdir, outfilename))
    return image



class Library(object):
    def __init__(self):
        self.presets = {}

    def register(self, name, preset):
        if self.presets.has_key(name):
            raise KeyError('Preset with name "%s" already registered' % name)
        self.presets[name] = preset

    def register_once(self, name, preset):
        try:
            self.register(name, preset)
        except KeyError:
            pass

    def unregister(self, name):
        self.presets.pop(name)

    def get(self, name):
        return self.presets[name]


library = Library()


