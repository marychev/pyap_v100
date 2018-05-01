# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-30 16:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings_template', '0003_auto_20180430_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='settingstemplate',
            name='meta',
            field=models.TextField(blank=True, help_text='\nПример: "Подключение meta тэга для \'Подтверждение прав на САЙТА\' в Яндекс-Вебмастер"<br>\n--------------------------------------------------------<br> \n<meta name="yandex-verification" content="831t65hfbfafdzyx" />\n', null=True, verbose_name='Блок Мета-тегов'),
        ),
    ]