"""
batch processing presets

@author: Marcin Nowak (marcin.j.nowak@gmail.com)
"""

import os
from cache import ImageCache

class Preset(object):
    """
    represents named preset
    """
    def __init__(self, name, processor, cached=False, output_dir=None):
        """
        initializes preset with processor, optional cache support
        """
        self.name = name
        self.cached = cached
        self._output_dir = output_dir
        self._cache = None
        self.processor = processor

    @property
    def cache(self):
        """
        returns image cache instance
        """
        if self.cached and not self._cache:
            self._cache = ImageCache(self.output_dir)
        return self._cache

    @property
    def output_dir(self):
        """
        returs output dir
        """
        if not self._output_dir:
            import settings
            self._output_dir = os.path.join(settings.PRESETS_ROOT, self.name)
            if not os.path.isdir(self._output_dir):
                os.makedirs(self._output_dir, 0777)
        return self._output_dir

    def _compute_dest_path(self, source):
        return os.path.join(self.output_dir, 
                os.path.basename(source))

    def get_image(self, source_file):
        """
        returns processed PIL Image instance for specified source file
        """
        if self.cached:
            return self.cache.get_image(self.processor, source_file,
                   self._compute_dest_path(source_file))
        return self.processor.process(source_file).save(self._compute_dest_path(source_file))
        
    def get_image_file(self, source_file):
        """
        returns processed image path for specified source file
        """
        if self.cached:
            return self.cache.get_image_file(self.processor, source_file,
                    self._compute_dest_path(source_file))
        return self.processor.process(source_file).save(self._compute_dest_path(source_file)).filename


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


# default presets
__DEFAULT_PRESETS = PresetsRegistry()

def create_preset(name, processor, cached=True, output_dir=None):
    """
    wrapper for easy presets creating and registering
    """
    __DEFAULT_PRESETS.register_once(name, Preset(name, processor, cached=cached, output_dir=output_dir))

def remove_preset(name):
    """
    wrapper for easy presets removing
    """
    __DEFAULT_PRESETS.unregister(name)

def get_preset(name):
    """
    wrapped for easy preset access
    """
    return __DEFAULT_PRESETS.get(name)
