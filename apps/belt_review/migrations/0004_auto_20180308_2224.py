# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-08 22:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('belt_review', '0003_book_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_image',
            field=models.FileField(blank=True, upload_to='post_images'),
        ),
    ]
