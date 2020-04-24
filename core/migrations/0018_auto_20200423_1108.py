# Generated by Django 2.2.8 on 2020-04-23 14:08

import core.models
from django.db import migrations, models
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_projetos_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='sobre',
            name='imagem',
            field=stdimage.models.StdImageField(default=4, upload_to=core.models.get_file_path, verbose_name='Imagem'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projetos',
            name='link',
            field=models.TextField(choices=[('project-1', 'projeto1'), ('project-2', 'projeto2'), ('project-3', 'projeto3'), ('project-4', 'projeto4'), ('project-5', 'projeto5'), ('project-6', 'projeto6'), ('project-7', 'projeto7'), ('project-8', 'projeto8')], max_length=12, unique=True, verbose_name='Area'),
        ),
    ]
