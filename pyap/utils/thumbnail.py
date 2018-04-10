import os, glob
from PIL import Image, ImageOps
from django.utils.safestring import mark_safe
from PIL import Image, ImageEnhance
from django.conf import settings
from filebrowser.sites import site
from filebrowser.base import FileObject


def get_thumbnail_url(image_url, size=150):
    # thumbs_part = 'thumbs_' + str(size)
    # image_url_parts = image_url.rsplit('/', 1)
    # return image_url_parts[0] + '/' + thumbs_part + '/' + image_url_parts[1]
    image_url_parts = image_url.rsplit('/', 1)
    return image_url_parts[0] + '/' + '/' + image_url_parts[1]


def get_thumbnail_path(image_path, size=150):
    thumbs_dir = 'thumbs_' + str(size)
    dirname, filename = os.path.split(image_path)
    dirname = os.path.join(dirname, thumbs_dir)
    if not os.path.exists(dirname):
        os.mkdir(dirname, 0x0755)
    return os.path.join(dirname, filename)


def create_thumbnail(image_path, size=150):
    thumb_path = get_thumbnail_path(image_path, size)
    delete_thumbnail(image_path, size)
    img = Image.open(image_path)
    img.thumbnail((size, size), Image.ANTIALIAS)
    img.save(thumb_path)


def delete_thumbnail(image_path, size=150):
    thumb_path = get_thumbnail_path(image_path, size)
    if os.path.exists(thumb_path):
        os.remove(thumb_path)


def resize(image_path, size, square=None):
    image_path = '{}/{}'.format(settings.MEDIA_ROOT, image_path)
    img = Image.open(image_path)
    if not square:
        img.thumbnail(size, Image.ANTIALIAS)
    else:
        img = ImageOps.fit(img, (50, 50), Image.ANTIALIAS)
    img.save(image_path)


def get_thumb(image):
    """вернуть миниатюру ***ADMIN***"""
    from django.conf import settings
    if image:
        fileobject = FileObject(os.path.join(site.directory, '', image.name))
        link = '{}{}'.format(settings.MEDIA_URL, fileobject.version_path("admin_thumbnail"))
        return mark_safe('<img src="{}">'.format(link))
    #     link = '<img src="%s">'
    #     return mark_safe(link % get_thumbnail_url(image.url))
    #     # return mark_safe(link % (image.url, get_thumbnail_url(image.url)))


def add_watermark(image, watermark, opacity=0.6, wm_interval=0, one=True):
    """ -------------------------------
    !!!! ДОРАБОТАТЬ !!!!!
    ------------------------------
    image - картинка, на которую накладываете изображение
    watermark - картинка, которую накладываете
    opacity - прозрачность
    wm_interval - интервал между изображениями watermark
    one - True = не размножать

    !!! watermark накладывается рекурсивно по всему полю изображения.
        Функция возвращает уже готовое изображение, которое надо еще сохранить.
    !!! если что-то не получается, сперва проверьте, может ли ваш PIL обрабатывать изображения jpeg, png, gif.
        бывает что PIL установлен, но всем любимые форматы вовсе не поддерживает, т.к. не (корректно) установлен libjpeg и т.п.
    """

    assert opacity >= 0 and opacity <= 1
    if opacity < 1:
        if watermark.mode != 'RGBA':
            watermark = watermark.convert('RGBA')
        else:
            watermark = watermark.copy()
        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        watermark.putalpha(alpha)

    layer = Image.new('RGBA', image.size, (0, 0, 0, 0))

    if one:
        # position: ```top_left```
        x = int(image.size[0] - image.size[0])
        y = int(image.size[1] - image.size[1])
        layer.paste(watermark, (x, y))
    else:
        for y in range(0, image.size[1], watermark.size[1]+wm_interval):
            for x in range(0, image.size[0], watermark.size[0]+wm_interval):
                layer.paste(watermark, (x, y))
    return Image.composite(layer,  image,  layer)

