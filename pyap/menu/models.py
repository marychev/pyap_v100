from __future__ import unicode_literals
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from catalog.models import Catalog
from blog.models import Blog
from page.models import Page
from gallery.models import Gallery
from utils.help_text import SORT_HT


class MainMenu(MPTTModel):
    """
    Модель Меню.
    Подержка вложенности.
    """
    name = models.CharField(max_length=80, null=True, verbose_name='название', db_index=True)
    parent = TreeForeignKey(
        'self', null=True, blank=True, related_name='child', verbose_name='родительская категория',
        on_delete=models.SET_NULL)
    is_show = models.BooleanField(default=True, verbose_name='Отображать')
    catalog = models.ForeignKey(Catalog, blank=True, null=True, verbose_name='каталог', on_delete=models.SET_NULL)
    blog = models.ForeignKey(Blog,  blank=True, null=True, verbose_name=' Blog',  on_delete=models.SET_NULL)
    page = models.ForeignKey(Page, blank=True, null=True, verbose_name='страница', on_delete=models.SET_NULL)
    gallery = models.ForeignKey(Gallery, blank=True, null=True, verbose_name='Галерея', on_delete=models.SET_NULL)
    sort = models.SmallIntegerField(default=1000, verbose_name='Сортировка', help_text=SORT_HT)

    def __str__(self):
        return self.name

    def get_url(self):
        """Вернуть ``slug`` приявязанного объекта, каталога, страницы, блога..."""
        slug = '/'
        if self.catalog:
            slug = self.catalog.get_absolute_url()
        if self.blog:
            slug = self.blog.get_absolute_url()
        if self.gallery:
            slug = self.gallery.get_absolute_url()
        if self.page:
            slug = self.page.get_absolute_url()
        return slug

    class Meta:
        unique_together = ('name', 'parent', 'is_show')
        verbose_name = 'пункт меню'
        verbose_name_plural = 'пункты меню'

    class MPTTMeta:
        order_insertion_by = ('parent', 'sort')

    # TODO: воссоздать метод. Перенести из утилиты
    #  def get_absolute_url(self):
    #     return reverse('product:product-detail', args=[self.product.catalog.first().url, self.product.url])
