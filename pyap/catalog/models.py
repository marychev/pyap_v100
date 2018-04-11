from django.db import models
from django.core.urlresolvers import reverse
from mptt.models import MPTTModel, TreeForeignKey
from utils.abstract_model import ABSContentModel, ABSImageModel
from site_info.models import Tag


class Catalog(MPTTModel, ABSContentModel):
    """
    Каталог. Поддерживает вложенность. Привязка товаров:model:`product.Product`.
    """

    parent = TreeForeignKey(
        'self', null=True, related_name='subitems', blank=True, db_index=True, verbose_name='Родительская категория')
    tags = models.ManyToManyField(Tag, verbose_name='Тэги', blank=True)

    # ---------------------------------------------------------------------------------
    # [!] Повторяются методы, если у модельи есть привязка к модели его фотографий ---
    # ---------------------------------------------------------------------------------
    def get_main_image(self):
        """
        Если модель имеет фотографии то этот метод должен быть!
        Вернуть главную, или 1ю.
        """
        images = CatalogImage.objects.filter(catalog_id=self.id)
        if images:
            image = images.first()
            if images.filter(image_is_main=True).exists():
                image = images.filter(image_is_main=True).first()
            return image

    def get_images(self):
        """
        Вернуть все фотографии объекта
        """
        return CatalogImage.objects.filter(catalog_id=self.id)
    # -----------------------------------------------------------------------------------

    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug,
        }
        return reverse('catalog:catalog', kwargs=kwargs)

    class Meta:
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталога'
        unique_together = ('title', 'parent', 'slug')

    class MPTTMeta:
        order_insertion_by = ('parent', 'sort')


class CatalogImage(ABSImageModel):
    """
    Фотографии для раздела Каталог
    """
    catalog = models.ForeignKey(Catalog, verbose_name='Каталог')

    def __str__(self):
        return self.catalog.title

    def save(self, *args, **kwargs):
        self.set_image_title(obj=self.catalog)
        super(CatalogImage, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Фотографию'
        verbose_name_plural = 'Фотографии'
