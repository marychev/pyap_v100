# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-13 23:47
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings_template', '0005_settingstemplate_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settingstemplate',
            name='terms_of_use',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Пользовотельское соглашение'),
        ),
    ]
