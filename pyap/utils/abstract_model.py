from django.conf import settings
from django.db import models
from filebrowser.fields import FileBrowseField
from ckeditor_uploader.fields import RichTextUploadingField
from utils.translit_field import translaton_field
from utils.help_text import SLUG_HT, SORT_HT, SEO_TITLE_HT, SEO_KEYWORDS_HT, SEO_DESCRIPTION_HT, OG_LOCALE_HT, \
    SWTTINGSTEMPLATE_SCRIPTS_HT
from users.models import User


class ABSTitleModel(models.Model):
    """
    Абстракная модель для полелй с названием и описанием объекта
    """
    title = models.CharField(max_length=255, db_index=True, null=True, verbose_name='Название*')
    description = models.TextField(verbose_name='Описание (информация)', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class ABSImageModel(models.Model):
    """
    Абстрактная модель для объекта с изображением
    """
    image = FileBrowseField(
        max_length=500, extensions=['.jpg', '.jpeg', '.png', '.gif'], blank=True, null=True, verbose_name='фото',
        help_text='Только форматы: ``.jpg, .jpeg, .png или .gif``')
    image_title = models.CharField(max_length=255, verbose_name='Название фото', blank=True, null=True)
    image_is_main = models.BooleanField(
        default=False, verbose_name='Главное', help_text='Главным может быть только одно фото')
    image_description = models.TextField(verbose_name='Краткое описание фото', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.set_image_title()
        super(ABSImageModel, self).save(*args, **kwargs)

    def set_image_title(self, obj=None):
        """
        Установить название фото. Если пусто - установить переданный `title` объекта
        Если объект не передан объекто считается `self`
        Установить главное изображение, если таого нет
        :param obj: {object} - QuerySet object
        """
        obj = obj if obj else self
        if hasattr(obj, 'title'):
            if not self.image_title and obj.title:
                self.image_title = obj.title
        if hasattr(obj, 'get_images'):
            if not obj.get_images().filter(image_is_main=True).exists():
                self.image_is_main = True

    # ---------------------------------------------------------------------------------
    # [!] Повторяются методы. Если у модели есть привязка к модели его фотографий ---
    # ---------------------------------------------------------------------------------
    def get_main_image(self):
        """
        Если модель имеет фотографии то этот метод должен быть!
        Вернуть главную, или 1ю.
        """
        return self.image if self.image else None

    class Meta:
        verbose_name = 'Фотографию'
        verbose_name_plural = 'Фотографии'
        ordering = 'image_is_main'
        abstract = True


# --- HELP TEXTS ---
# ---------------------


class SeoModel(models.Model):
    """
    Сео настройки для объекта модели
    """
    slug = models.SlugField(verbose_name='элемент URL', db_index=True, help_text=SLUG_HT)
    seo_title = models.CharField(
        max_length=255, verbose_name='Seo title', blank=True, null=True, help_text=SEO_TITLE_HT)
    seo_description = models.TextField(
        max_length=510, verbose_name='Seo description', blank=True, null=True, help_text=SEO_DESCRIPTION_HT)
    seo_keywords = models.TextField(
        max_length=510, verbose_name='Seo keywords', blank=True, null=True, help_text=SEO_KEYWORDS_HT)
    og_locale = models.TextField(
        max_length=510, null=True, blank=True, default='ru_RU', verbose_name='og locale', help_text=OG_LOCALE_HT)
    scripts = models.TextField(
        null=True, blank=True, verbose_name="Блок скриптов", help_text=SWTTINGSTEMPLATE_SCRIPTS_HT)

    def save(self, *args, **kwargs):
        from utils.auto_seo import AutoSeo
        AutoSeo(page=self, title=self.title).default()
        # обрезать `slug` если симоволов больше 255
        if len(self.slug) > 255:
            short_title = '[!] {}'.format(self.title[:251])
            self.slug = translaton_field(short_title)
        super(SeoModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class CreatedUpdatedModel(models.Model):
    """
    Дата создания и обновления объекта модели
    """
    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обнавлен', auto_now=True)

    class Meta:
        abstract = True


class ABSCommentModel(CreatedUpdatedModel):
    """
    Коментарии к к объекту, Например коментирование поста, или пользователя
    """
    text = models.TextField(verbose_name='Комментарий')
    ip_address = models.GenericIPAddressField(default='0.0.0.0', verbose_name='IP address', null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name='Пользователь')
    username = models.CharField(max_length=125, default='anonymous', blank=True, null=True, verbose_name='Имя пользователя')
    email = models.EmailField(blank=True, verbose_name='Email')
    is_show = models.BooleanField(default=False, verbose_name='Отображать')

    def __str__(self):
        return self.text

    class Meta:
        abstract = True
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
        ordering = ('created',)


class ABSContentModel(ABSTitleModel, SeoModel, CreatedUpdatedModel):
    """
    Абстракная модель для полелй с названием, описанием объекта , HTML контентом
    """
    html = RichTextUploadingField(verbose_name='HTML/Текст', blank=True, null=True)
    sort = models.SmallIntegerField(default=1000, verbose_name='Сортировка', help_text=SORT_HT)
    is_show = models.BooleanField(default=True, verbose_name='Отображать')
    author = models.ForeignKey(User, verbose_name='Автор',blank=True, null=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        from utils.auto_seo import AutoSeo
        AutoSeo(page=self, title=self.title).default()
        super(ABSContentModel, self).save(*args, **kwargs)

    class Meta:
        ordering = 'sort'
        abstract = True
