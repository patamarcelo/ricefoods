# Generated by Django 2.2.8 on 2020-04-20 11:10

import core.models
from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200420_0807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicos',
            name='imagem',
            field=stdimage.models.StdImageField(upload_to=core.models.get_file_path, verbose_name='Imagem'),
        ),
    ]
