# Generated by Django 4.0.1 on 2022-06-26 17:02

import core.models
from django.db import migrations, models
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20200423_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projetos',
            name='imagem',
            field=stdimage.models.StdImageField(force_min_size=False, upload_to=core.models.get_file_path, variations={'thumb': {'crop': True, 'height': 702, 'width': 722}}, verbose_name='Imagem'),
        ),
        migrations.AlterField(
            model_name='servicos',
            name='imagem',
            field=stdimage.models.StdImageField(force_min_size=False, upload_to=core.models.get_file_path, variations={'thumb': {'crop': True, 'height': 398, 'width': 690}}, verbose_name='Imagem'),
        ),
        migrations.AlterField(
            model_name='sobre',
            name='imagem',
            field=stdimage.models.StdImageField(force_min_size=False, upload_to=core.models.get_file_path, variations={'thumb': {'crop': True, 'height': 1280, 'width': 1920}}, verbose_name='Imagem'),
        ),
        migrations.AlterField(
            model_name='sobretopico',
            name='icone',
            field=models.TextField(choices=[('fa-binoculars', 'binoculos'), ('fa-list-alt', 'lista'), ('fa-chart-pie', 'grafico pizza'), ('fa-truck', 'caminhão'), ('fa-warehouse', 'armazem')], max_length=18, verbose_name='Icone'),
        ),
        migrations.AlterField(
            model_name='subprojetos',
            name='imagem',
            field=stdimage.models.StdImageField(force_min_size=False, upload_to=core.models.get_file_path, variations={'thumb': {'crop': True, 'height': 1280, 'width': 1920}}, verbose_name='Imagem'),
        ),
    ]
