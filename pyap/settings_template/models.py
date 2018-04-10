from django.db import models
from django.contrib.sites.models import Site
from filebrowser.fields import FileBrowseField
from catalog.models import Catalog
from page.models import Page
from home.models import Home
from blog.models import Blog
from gallery.models import Gallery
from site_info.models import ListLink, TextInfo
from utils.help_text import ROBOTS_TXT_HT, SWTTINGSTEMPLATE_TITLE_HT, SWTTINGSTEMPLATE_PHONE_HT, \
    SWTTINGSTEMPLATE_IS_INCLUDED_HT, SWTTINGSTEMPLATE_LOGO_HT, SWTTINGSTEMPLATE_SCRIPTS_HT


class Footer(models.Model):
    """
    футера. Блок текста/блок ссылок(тегов).
    """
    title = models.CharField(
        max_length=125, verbose_name='Заголовок', unique=True, default='Нижний футер')
    list_link = models.ManyToManyField(ListLink, verbose_name='Быстрые ссылки', blank=True)
    text_info = models.ForeignKey(TextInfo, verbose_name='Текстовое оформление', blank=True, null=True)
    catalog = models.ManyToManyField(
        Catalog, verbose_name='Каталоги', limit_choices_to={'is_show': True}, blank=True)
    page = models.ManyToManyField(
        Page, verbose_name='Страницы', limit_choices_to={'is_show': True}, blank=True)
    blogs = models.ManyToManyField(
        Blog, verbose_name='Блоги', limit_choices_to={'is_show': True}, blank=True)
    galleries = models.ManyToManyField(
        Gallery, verbose_name='Галереи', limit_choices_to={'is_show': True}, blank=True)
    is_show = models.BooleanField(default=True, verbose_name='Отображать')

    def __str__(self):
        return self.title

    def get_list_link(self):
        return self.list_link.filter(is_show=True)

    class Meta:
        verbose_name = 'футер'
        verbose_name_plural = 'настрока футера'


class SettingsTemplate(models.Model):
    """
    Основные настройки шаблона
    """
    site = models.OneToOneField(Site, verbose_name='Сайт/Домен', blank=True, null=True)
    title = models.CharField(
        max_length=125, verbose_name='Заголовок', unique=True,
        help_text=SWTTINGSTEMPLATE_TITLE_HT, default='Основной шаблон')
    home = models.ForeignKey(Home, verbose_name='Главная страница', blank=True, null=True)
    footer = models.ForeignKey(Footer, verbose_name='футер', blank=True, null=True)
    is_included = models.BooleanField(default=False, verbose_name='Включена', help_text=SWTTINGSTEMPLATE_IS_INCLUDED_HT)
    phone = models.CharField(
        max_length=30, blank=True, null=True, verbose_name='Номер телефона',
        help_text=SWTTINGSTEMPLATE_PHONE_HT, unique=True)
    address = models.CharField(max_length=255, default="Адрес", blank=True, null=True, verbose_name="Адрес")
    logo = FileBrowseField(
        "Логотип", max_length=500, extensions=[".png", '.jpg', '.jpeg', ".gif"],
        blank=True, null=True, help_text=SWTTINGSTEMPLATE_LOGO_HT)
    robots_txt = models.TextField(
        null=True, blank=True, verbose_name="Содержимое robots.txt",
        default=ROBOTS_TXT_HT, help_text=ROBOTS_TXT_HT)
    terms_of_use = models.TextField(null=True, blank=True, verbose_name="Пользовотельское соглашение")
    scripts = models.TextField(
        null=True, blank=True, verbose_name="Блок скриптов", help_text=SWTTINGSTEMPLATE_SCRIPTS_HT)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'настройку шаблона'
        verbose_name_plural = 'основные настройка шаблона'
