from django.db import models
from filebrowser.fields import FileBrowseField
from utils.help_text import URL_HT, SORT_HT


class SliderHome(models.Model):
    """ Слайдер главной страницы """
    class Meta:
        ordering = ('sort',)
        verbose_name = 'слайды'
        verbose_name_plural = 'слайдер'

    title = models.CharField(max_length=126, verbose_name='Название', blank=True, null=True)
    description = models.TextField(max_length=1024, verbose_name='Описание', null=True, blank=True)
    image = FileBrowseField(max_length=500, extensions=['.jpg', '.jpeg', '.png', '.gif'], verbose_name='Изображение')
    url = models.URLField('Полный путь к веб-странице', null=True, blank=True, help_text=URL_HT)
    sort = models.PositiveSmallIntegerField('Сортировка', null=True, blank=True, help_text=SORT_HT, default=1000)

    def __str__(self):
        return self.title

    def get_description(self):
        return self.description


# [!] NOT DELETE ---
# -------------------

# image = models.ImageField(upload_to='slider/', verbose_name='Изображение')

# def save(self, *args, **kwargs):
#     from sorl.thumbnail import ImageField, delete, get_thumbnail
#     from utils.thumbnail import resize, get_thumb
#     super(SliderHome, self).save(*args, **kwargs)
#     if self.image and (self.image.width > 1400 or self.image.height > 1000):
#         resize(self.image.path, (1400, 1000))
