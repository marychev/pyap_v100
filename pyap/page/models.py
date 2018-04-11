from django.db import models
from django.core.urlresolvers import reverse
from utils.abstract_model import ABSContentModel, ABSImageModel, ABSCommentModel
from site_info.models import Tag


class Page(ABSContentModel):
    """
    Модель для контент-страниц, таких как О нас, Контакты...
    """
    is_allow_comments = models.BooleanField(default=False, verbose_name='разрешить комментарии')
    tags = models.ManyToManyField(Tag, verbose_name='Тэги', blank=True)

    class Meta:
        unique_together = ('slug', 'created')
        verbose_name = 'страница'
        verbose_name_plural = 'страницы'

    def get_absolute_url(self):
        return reverse('page:page-detail', args=[self.slug])

    def get_comments(self):
        qs = PageComment.objects.filter(page_id=self.id)
        return qs
    # ---------------------------------------------------------------------------------
    # [!] Повторяются методы, если у модельи есть привязка к модели его фотографий ---
    # ---------------------------------------------------------------------------------
    def get_main_image(self):
        """
        Если модель имеет фотографии то этот метод должен быть!
        Вернуть главную, или 1ю.
        """
        images = PageImage.objects.filter(page_id=self.id)
        if images:
            image = images.first()
            if images.filter(image_is_main=True).exists():
                image = images.filter(image_is_main=True).first()
            return image

    def get_images(self):
        """
        Вернуть все фотографии объекта
        """
        return PageImage.objects.filter(page_id=self.id)
    # -----------------------------------------------------------------------------------


class PageImage(ABSImageModel):
    """
    Фотографии для Страницы :model:`page.Page`.
    """
    page = models.ForeignKey(Page, verbose_name='Страница')

    def save(self, *args, **kwargs):
        self.set_image_title(obj=self.page)
        super(PageImage, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Фотографию'
        verbose_name_plural = 'Фотографии'


class PageComment(ABSCommentModel):
    """
    Коментарии к контент-странице
    """
    page = models.ForeignKey(Page, verbose_name='Страница', null=True, on_delete=models.SET_NULL)
