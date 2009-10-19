"""
Image presets presets module
author: Marcin Nowak (marcin.j.nowak@gmail.com)
"""

import os
from cache import ImageCache

class Preset(object):
    def __init__(self, name, processor, cached=False, output_dir=None):
        self.name = name
        self.cached = cached
        self._output_dir = output_dir
        self._cache = None
        self.processor = processor

    @property
    def cache(self):
        if self.cached and not self._cache:
            self._cache = ImageCache(self.output_dir)
        return self._cache

    @property
    def output_dir(self):
        if not self._output_dir:
            import settings
            self._output_dir = os.path.join(settings.PRESETS_ROOT, self.name)
            if not os.path.isdir(self._output_dir):
                os.makedirs(self._output_dir, 0777)
        return self._output_dir

    def _compute_dest_path(self, source):
        return os.path.join(self.output_dir, 
                os.path.basename(source))

    def get_image(self, file):
        if self.cached:
            return self.cache.get_image(self.processor, file,
                   self._compute_dest_path(file))
        return self.processor.process(file).save(self._compute_dest_path(file))
        
    def get_image_file(self, file):
        if self.cached:
            return self.cache.get_image_file(self.processor, file,
                    self._compute_dest_path(file))
        return self.processor.process(file).save(self._compute_dest_path(file)).filename


class PresetsRegistry(object):
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


__default_presets = PresetsRegistry()

def create_preset(name, processor, cached=True, output_dir=None):
    __default_presets.register_once(name, Preset(name, processor, cached=cached, output_dir=output_dir))

def remove_preset(name):
    __default_presets.unregister(name)

def get_preset(name):
    return __default_presets.get(name)
