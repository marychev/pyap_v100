# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-29 19:11
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filebrowser.fields
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255, null=True, verbose_name='Название*')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание (информация)')),
                ('slug', models.SlugField(help_text='генерируется автоматически', verbose_name='элемент URL')),
                ('seo_title', models.CharField(blank=True, help_text='Предпочтительное значение 50-80 символов', max_length=255, null=True, verbose_name='Seo title')),
                ('seo_description', models.TextField(blank=True, help_text='Предпочтительное значение 150-200 символов', max_length=510, null=True, verbose_name='Seo description')),
                ('seo_keywords', models.TextField(blank=True, help_text='Ориентируйтесь на ударные первые 150 знаков, 250 максимум', max_length=510, null=True, verbose_name='Seo keywords')),
                ('og_locale', models.TextField(blank=True, default='ru_RU', help_text='\nгруппа мета-тегов, рассказывающая социальным сетям о содержимом страниц, которыми вы делитесь.\nБлагодаря этому ссылки из набора символов превращаются в понятные заголовки с картинками и пояснениями.\n<code>\n    <meta property="og:url" content="http://www.mysite.ru/2015/02/19/arts/international/page.html" />\n    <meta property="og:type" content="article" />\n    <meta property="og:title" content="When Great Minds Don’t Think Alike" />\n    <meta property="og:description" content="How much does culture influence creative thinking?" />\n    <meta property="og:image" content="http://mysite.com/static/img/2015/02/19/img.jpg" />\n</code>\n', max_length=510, null=True, verbose_name='og locale')),
                ('scripts', models.TextField(blank=True, help_text='\nПример: "Подключение CSS фрэймворка - Bootstrap 4.0"<br>\n--------------------------------------------------------<br> \n< script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script><br>\n< script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script><br>\n< script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>\n', null=True, verbose_name='Блок скриптов')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обнавлен')),
                ('html', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='HTML/Текст')),
                ('sort', models.SmallIntegerField(default=1000, help_text='<br><i>\nЛучше использовать за единицу сортировки 1000 или 100.. \nТак проще будет разобраться, если элементы имеют большую вложенность.<br>\nИли придумайте свою систему сортировки : )\n<br>ПРИМЕР - 1000:__________________ПРИМЕР - 2000:\n<br>.... Пример - 1100__________________.... Пример - 2200\n<br>........... пример - 1110__________________........ пример - 2220\n<br>............... пример - 1111__________________............... пример - 2222</i>\n', verbose_name='Сортировка')),
                ('is_show', models.BooleanField(default=True, verbose_name='Отображать')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subitems', to='catalog.Catalog', verbose_name='Родительская категория')),
            ],
            options={
                'verbose_name_plural': 'Категории',
                'verbose_name': 'Категорию',
            },
        ),
        migrations.CreateModel(
            name='CatalogImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', filebrowser.fields.FileBrowseField(blank=True, help_text='Только форматы: ``.jpg, .jpeg, .png или .gif``', max_length=500, null=True, verbose_name='фото')),
                ('image_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название фото')),
                ('image_is_main', models.BooleanField(default=False, help_text='Главным может быть только одно фото', verbose_name='Главное')),
                ('image_description', models.TextField(blank=True, null=True, verbose_name='Краткое описание фото')),
                ('catalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Catalog', verbose_name='Каталог')),
            ],
            options={
                'verbose_name_plural': 'Фотографии',
                'verbose_name': 'Фотографию',
            },
        ),
        migrations.AlterUniqueTogether(
            name='catalog',
            unique_together=set([('title', 'parent', 'slug')]),
        ),
    ]
