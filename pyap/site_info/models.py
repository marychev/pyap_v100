from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from filebrowser.fields import FileBrowseField
from utils.thumbnail import resize
from utils.abstract_model import ABSImageModel
from utils.help_text import SETTINGSTEMPLATE_TYPE_LINK_HT, SOCIAL_NETWORK_HTML_LINK_HT


class TextInfo(models.Model):
    """Текстовая информация"""
    class Meta:
        verbose_name = 'текстовая информация'
        verbose_name_plural = 'текстовые информации'

    title = models.CharField(max_length=125, verbose_name='Заголовок', unique=True)
    html = RichTextUploadingField(verbose_name='Текст/HTML')

    def __str__(self):
        return self.title


class ListLink(models.Model):
    """Быстрые ссылки"""
    LINK = 'L'
    TAG = 'T'
    TYPE_LINK_CHOICES = (
        (LINK, 'ссылки'),
        (TAG, 'тэги')
    )

    class Meta:
        verbose_name = 'быстрая ссылка'
        verbose_name_plural = 'быстрые ссылки'

    title = models.CharField(max_length=125, verbose_name='Заголовок', db_index=True)
    url = models.URLField(max_length=255, verbose_name='URL страницы', blank=True, null=True, db_index=True)
    sort = models.PositiveSmallIntegerField(verbose_name='Порядок отображения', db_index=True, default=0)
    is_show = models.BooleanField(default=True, verbose_name='Показать/Скрыть')
    type_link = models.CharField(
        max_length=1, choices=TYPE_LINK_CHOICES, default=TYPE_LINK_CHOICES[0], verbose_name='Вид ссылки',
        help_text=SETTINGSTEMPLATE_TYPE_LINK_HT)

    def __str__(self):
        return self.title


class SocialNetwork(ABSImageModel):
    """
    Настрока социальных сетей приложения, сайта
    """
    title = models.CharField(max_length=255, verbose_name='Заголовок', blank=True, null=True)
    image = FileBrowseField(max_length=512, extensions=['.jpg', '.jpeg', '.png', '.gif'], verbose_name='Иконка', blank=True, null=True)
    html_link = models.CharField(
        verbose_name='НТМЛ-ссылка', max_length=512, unique=True, blank=True, null=True,
        help_text=SOCIAL_NETWORK_HTML_LINK_HT)
    url = models.URLField(verbose_name='URL страницы', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_html_links(self):
        """Получить все ссылки, заключенные в HTML код."""
        return SocialNetwork.objects.filter(image__isnull=True, html_link__isnull=False).values('html_link',)

    def save(self, *args, **kwargs):
        super(SocialNetwork, self).save(*args, **kwargs)
        # --resizing image
        if self.image and (self.image.width > 200 or self.image.height > 200):
            resize(self.image.path, (200, 200), True)

    class Meta:
        verbose_name = 'социальная сеть'
        verbose_name_plural = 'социальные сети'
