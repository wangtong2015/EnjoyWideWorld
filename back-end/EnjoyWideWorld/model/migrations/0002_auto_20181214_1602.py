# Generated by Django 2.1.4 on 2018-12-14 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='position_picture',
            field=models.ImageField(default=None, null=True, upload_to='./position/'),
        ),
    ]
