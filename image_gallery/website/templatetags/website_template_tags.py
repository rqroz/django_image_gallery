from django import template
from django.contrib.auth.models import Group
import os.path
from PIL import Image

register = template.Library()

FMT = 'JPEG'
EXT = 'jpg'
QUAL = 100

@register.filter
def is_manager(user):
    return user.data.is_manager()

def resized_path(path, size, method):
    "Returns the path for the resized image."
    dir, name = os.path.split(path)
    image_name, ext = name.rsplit('.', 1)
    return os.path.join(dir, '%s_%s_%s.%s' % (image_name, method, size, EXT))

@register.filter
def scale_img(image_field, size, method='scale'):
    """
    Template filter used to scale an image
    that will fit inside the defined area.

    Returns the url of the resized image.

    {% load image_tags %}
    {{ profile.picture|scale:"48x48" }}
    """

    image_path = resized_path(image_field.path, size, method)

    if not os.path.exists(image_path):
        image = Image.open(image_field.path)

        # parse size string 'WIDTHxHEIGHT'
        width, height = [int(i) for i in size.split('x')]

        # use PIL methods to edit images
        if method == 'scale':
            image.thumbnail((width, height), Image.ANTIALIAS)
            image.save(image_path, FMT, quality=QUAL)

        elif method == 'crop':
            try:
                import ImageOps
            except ImportError:
                from PIL import ImageOps

            ImageOps.fit(image, (width, height), Image.ANTIALIAS).save(image_path, FMT, quality=QUAL)

    return resized_path(image_field.url, size, method)


@register.filter
def crop_img(image_field, size):
    """
    Template filter used to crop an image
    to make it fill the defined area.

    {% load image_tags %}
    {{ profile.picture|crop:"48x48" }}

    """
    return scale_img(image_field, size, 'crop')
