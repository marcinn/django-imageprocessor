from processors import ImageProcessor, filter_spec, imageprocessor_from_preset
from cache import ImageCache, CachedImage
from presets import get_preset


def process_image(preset_name, filename):
    return imageprocessor_from_preset(
            get_preset(preset_name)).process(filename)


def get_cached_image(preset_name, image_path):
    """
    retrieve or transparently generate cache for full-sized image
    """
    
    preset = get_preset(preset_name)
    processor = imageprocessor_from_preset(preset)
    cache = ImageCache(preset.output_dir)
    img = cache.get_image(processor, image_path)
    if not img:
        img = CachedImage(processor.process(image_path).save().filename)
    return img


