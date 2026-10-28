import os
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image, ImageOps

IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
MIN_BYTES = 180 * 1024
JPEG_QUALITY = 82

IMAGE_FIELDS = {
    ('core', 'UserProfile'): ('avatar', 512),
    ('core', 'Post'): ('image', 1600),
    ('core', 'PostMedia'): ('file', 1600),
    ('core', 'BlogPost'): ('image', 1600),
    ('core', 'Community'): ('cover', 1600),
    ('core', 'TeamPortfolioProject'): ('image', 1600),
    ('core', 'Banner'): ('image', 1600),
}


def _extension(name):
    return name.rsplit('.', 1)[-1].lower() if '.' in name else ''


def _has_alpha(image):
    if image.mode in ('RGBA', 'LA'):
        return image.getchannel('A').getextrema()[0] < 255
    return image.mode == 'P' and 'transparency' in image.info


def optimize_field_file(field_file, max_side):
    if not field_file or not field_file.name:
        return None
    extension = _extension(field_file.name)
    if extension not in IMAGE_EXTENSIONS:
        return None
    storage = field_file.storage
    try:
        original_size = storage.size(field_file.name)
        with storage.open(field_file.name, 'rb') as handle:
            image = Image.open(handle)
            image.load()
    except Exception:
        return None
    if getattr(image, 'is_animated', False):
        return None
    if original_size < MIN_BYTES and max(image.size) <= max_side:
        return None

    image = ImageOps.exif_transpose(image)
    image.thumbnail((max_side, max_side), Image.LANCZOS)
    buffer = BytesIO()
    new_name = field_file.name
    if extension == 'png' and _has_alpha(image):
        image.save(buffer, 'PNG', optimize=True)
    elif extension == 'webp':
        image.save(buffer, 'WEBP', quality=JPEG_QUALITY, method=5)
    else:
        image.convert('RGB').save(buffer, 'JPEG', quality=JPEG_QUALITY, optimize=True, progressive=True)
        if extension == 'png':
            new_name = os.path.splitext(field_file.name)[0] + '.jpg'

    data = buffer.getvalue()
    if new_name == field_file.name and len(data) >= original_size:
        return None
    if new_name != field_file.name:
        new_name = storage.save(new_name, ContentFile(data))
    else:
        storage.delete(field_file.name)
        storage.save(field_file.name, ContentFile(data))
    return {'name': new_name, 'before': original_size, 'after': len(data)}


def optimize_instance(instance):
    config = IMAGE_FIELDS.get((instance._meta.app_label, instance.__class__.__name__))
    if not config:
        return None
    field_name, max_side = config
    if getattr(instance, 'media_type', 'image') != 'image':
        return None
    result = optimize_field_file(getattr(instance, field_name), max_side)
    if result and result['name'] != getattr(instance, field_name).name:
        type(instance).objects.filter(pk=instance.pk).update(**{field_name: result['name']})
        setattr(instance, field_name, result['name'])
    return result
