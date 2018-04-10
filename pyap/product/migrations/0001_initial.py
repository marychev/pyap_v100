# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-29 19:11
from __future__ import unicode_literals

import ckeditor_uploader.fields
from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import filebrowser.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
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
                ('articul', models.CharField(blank=True, max_length=256, null=True, unique=True, verbose_name='Артикул (уник)')),
                ('is_bestseller', models.BooleanField(default=False, verbose_name='Хит продаж')),
                ('is_new', models.BooleanField(default=True, verbose_name='Новинка')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('catalog', models.ManyToManyField(blank=True, to='catalog.Catalog', verbose_name='Категории')),
                ('recommend_products', models.ManyToManyField(blank=True, help_text='Отображаются внизу карточки товара, как рекомендованные или похожие товары', related_name='_product_recommend_products_+', to='product.Product', verbose_name='Рекомендованные/Похожие')),
            ],
            options={
                'verbose_name_plural': 'товары',
                'verbose_name': 'товар',
            },
        ),
        migrations.CreateModel(
            name='ProductComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обнавлен')),
                ('text', models.TextField(verbose_name='Сообщения')),
                ('ip_address', models.GenericIPAddressField(default='0.0.0.0', null=True, verbose_name='IP address')),
                ('username', models.CharField(blank=True, default='anonymous', max_length=125, null=True, verbose_name='Имя пользователя')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('is_show', models.BooleanField(default=False, verbose_name='Отображать')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.Product', verbose_name='Товар')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'ordering': ('created',),
                'verbose_name_plural': 'Коментарии',
                'abstract': False,
                'verbose_name': 'Коментарий',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', filebrowser.fields.FileBrowseField(blank=True, help_text='Только форматы: ``.jpg, .jpeg, .png или .gif``', max_length=500, null=True, verbose_name='фото')),
                ('image_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название фото')),
                ('image_is_main', models.BooleanField(default=False, help_text='Главным может быть только одно фото', verbose_name='Главное')),
                ('image_description', models.TextField(blank=True, null=True, verbose_name='Краткое описание фото')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Product', verbose_name='Товар')),
            ],
            options={
                'verbose_name_plural': 'Фотографии',
                'verbose_name': 'Фотографию',
            },
        ),
        migrations.CreateModel(
            name='ProductItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обнавлен')),
                ('name', models.CharField(help_text='Прим:размерный ряд', max_length=256, verbose_name='Наименование')),
                ('articul', models.CharField(blank=True, max_length=256, null=True, unique=True, verbose_name='Артикул (уникальный)')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0'))], verbose_name='Цена')),
                ('price_discount', models.DecimalField(decimal_places=2, default=0, help_text='Если указана - станет ценой продажи товара.', max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0'))], verbose_name='Акционная цена')),
                ('price_purchase', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0'))], verbose_name='Цена закупки')),
                ('quantity', models.IntegerField(default=0, verbose_name='Кол-во')),
                ('is_main', models.BooleanField(default=False, verbose_name='Главный')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Product', verbose_name='Главный товар')),
            ],
            options={
                'ordering': ('price',),
                'verbose_name_plural': 'Варианты продукта',
                'verbose_name': 'Вариант продукта',
            },
        ),
        migrations.AlterUniqueTogether(
            name='productitem',
            unique_together=set([('product', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set([('title', 'slug')]),
        ),
    ]
