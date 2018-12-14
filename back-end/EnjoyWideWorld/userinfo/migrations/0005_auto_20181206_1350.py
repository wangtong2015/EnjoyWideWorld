# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-12-06 13:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0004_auto_20181206_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='pet_picture',
            field=models.ImageField(default=None, upload_to='./pet/'),
        ),
        migrations.AlterField(
            model_name='position',
            name='position_picture',
            field=models.ImageField(default=None, upload_to='./position/'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='profile_picture',
            field=models.ImageField(default=None, upload_to='./user/'),
        ),
    ]