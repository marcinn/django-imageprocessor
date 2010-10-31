"""
batch processing presets

@author: Marcin Nowak (marcin.j.nowak@gmail.com)
"""

import os
import settings
import warnings


class Preset(object):
    """
    represents named preset
    """
    def __init__(self, name, filters, cached=False, output_dir=None, quality=75):
        """
        initializes preset with processor, optional cache support
        """
        if not output_dir:
            output_dir = os.path.join(settings.PRESETS_ROOT, name)

        self.name = name
        self.cached = cached
        self.output_dir = output_dir
        self.filters = filters
        self.quality = quality



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

def create_preset(name, filters, cached=True, output_dir=None):
    """
    wrapper for easy presets creating and registering
    """
    from processors import ImageProcessor
    if isinstance(filters, ImageProcessor):
         warnings.warn('Configure preset with filters not ImageProcessor instance',
                DeprecationWarning)
         filters = filters.filters
        
    __DEFAULT_PRESETS.register_once(name, Preset(name, filters, cached=cached, output_dir=output_dir))

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

def Filter(filter_instance, *args, **kwargs):
    """
    helper for easy adding filters as init arg for processor
    """
    return (filter_instance, args, kwargs)

