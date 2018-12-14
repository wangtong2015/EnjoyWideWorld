# Generated by Django 2.1.4 on 2018-12-14 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0002_auto_20181214_1602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='position',
            name='position_picture',
        ),
        migrations.AddField(
            model_name='item',
            name='addExp',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='position',
            name='pictureAddr',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
