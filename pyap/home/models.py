from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from utils.abstract_model import SeoModel, ABSImageModel
from blog.models import Blog


class Home(SeoModel):
    """
    Настройки главной страницы
    """
    class Meta:
        verbose_name = 'главная страница'
        verbose_name_plural = 'главная страница'

    title = models.CharField(max_length=255, verbose_name='Заголовок', unique=True, default='Главная страница')
    html = RichTextUploadingField(verbose_name='Контент/HTML', blank=True, null=True)
    blog = models.ForeignKey(
        Blog, verbose_name='Блог', blank=True, null=True,
        help_text='Например, создать блог ПОСЛЕДНЕИ НОВОСТИ и закрепить его на главную страницу. '
                  'Или выбрать из существующих')
    is_show = models.BooleanField(default=True, verbose_name='Отображать')

    def __str__(self):
        return self.title

    # ---------------------------------------------------------------------------------
    # [!] Повторяются методы, если у модельи есть привязка к модели его фотографий ---
    # ---------------------------------------------------------------------------------
    def get_main_image(self):
        """
        Если модель имеет фотографии то этот метод должен быть!
        Вернуть главную, или 1ю.
        """
        images = HomeImage.objects.filter(home_id=self.id)
        if images:
            image = images.first()
            if images.filter(image_is_main=True).exists():
                image = images.filter(image_is_main=True).first()
            return image

    def get_images(self):
        """
        Вернуть все фотографии объекта
        """
        return HomeImage.objects.filter(home_id=self.id)  # .values('image',)
    # -----------------------------------------------------------------------------------


class HomeImage(ABSImageModel):
    """
    Фотографии для раздела Главной страницы
    """
    home = models.ForeignKey(Home, verbose_name='Главная страница')

    def __str__(self):
        return self.home.title

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
