from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from filebrowser.fields import FileBrowseField


class UserProfile(models.Model):
    """
    Профиль. Дополнительные данные о пользователе
    """
    user = models.OneToOneField(User, verbose_name='Пользователь')
    avatar = FileBrowseField(
        max_length=500, extensions=['.jpg', '.jpeg', '.png', '.gif'], blank=True, null=True, verbose_name='Аватар')
    patronymic = models.CharField(max_length=155, blank=True, null=True, verbose_name='Отчество')
    birthday = models.DateField(verbose_name='День рождения', blank=True, null=True)
    phone = models.CharField(max_length=32, verbose_name='Телефон', blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True, verbose_name='Адрес')
    about = models.TextField(verbose_name='О себе', blank=True, null=True)
    id_signed_news = models.BooleanField(default=False, verbose_name='Подписан на новости')

    def __str__(self):
        return '{}'.format(self.user)

    def get_full_name(self):
        """Получить полное ФИО"""
        return '%s %s %s' % (self.user.last_name, self.user.first_name, self.patronymic)

    def get_short_name(self):
        """Получить только Фамилию и имя"""
        short_name = '{} {}'.format(self.user.last_name, self.user.first_name)
        return short_name if self.user.first_name else None


class UserLink(models.Model):
    """Модель для отдельных пользовательских ссылок"""
    user = models.ForeignKey(User, verbose_name='Пользователь')
    anchor = models.CharField(max_length=100, verbose_name='Название ссылки / текст привязки', blank=True, null=True)
    url = models.URLField(verbose_name='URL', blank=True, null=True)

    def __str__(self):
        return self.anchor
