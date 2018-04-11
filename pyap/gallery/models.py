from django.db import models
from django.core.urlresolvers import reverse
from mptt.models import MPTTModel, TreeForeignKey
from utils.abstract_model import ABSContentModel, ABSImageModel
from site_info.models import Tag


class Gallery(MPTTModel, ABSContentModel):
    """
    Модель Галерея. Поддерживает вложенность. Предназначена для привязки к одному объекту-разделу множество фотографий.
    Применение: подходит для создания различного рода вывода массого списка изображений.
    """
    parent = TreeForeignKey('self', blank=True, null=True, related_name='subitems', db_index=True, verbose_name='Галерея-родитель')
    tags = models.ManyToManyField(Tag, verbose_name='Тэги', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug,
            # 'year': '%04d' % self.created.year,
            # 'month': '%02d' % self.created.month,
            # 'day': '%02d' % self.created.day,
        }
        return reverse('gallery:gallery_detail', kwargs=kwargs)

    # ---------------------------------------------------------------------------------
    # [!] Повторяются методы, если у модельи есть привязка к модели его фотографий ---
    # ---------------------------------------------------------------------------------
    def get_main_image(self):
        """
        Если модель имеет фотографии то этот метод должен быть!
        Вернуть главную, или 1ю.
        """
        images = GalleryImage.objects.filter(gallery_id=self.id)
        if images:
            image = images.first()
            if images.filter(image_is_main=True).exists():
                image = images.filter(image_is_main=True).first()
            return image

    def get_images(self):
        """
        Вернуть все фотографии объекта
        """
        return GalleryImage.objects.filter(gallery_id=self.id)

    # -----------------------------------------------------------------------------------

    class Meta:
        verbose_name = 'Галерею'
        verbose_name_plural = 'Галереи'
        unique_together = ('title', 'parent', 'slug')

    class MPTTMeta:
        order_insertion_by = ('parent', 'sort')


class GalleryImage(ABSImageModel):
    """
    Фотографии для раздела Галереи
    """
    gallery = models.ForeignKey(Gallery, verbose_name='Галерея')

    def __str__(self):
        return self.gallery.title

    def save(self, *args, **kwargs):
        self.set_image_title(obj=self.gallery)
        super(GalleryImage, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Фотографию'
        verbose_name_plural = 'Фотографии'

