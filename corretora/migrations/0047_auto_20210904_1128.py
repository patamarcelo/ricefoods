# Generated by Django 2.2.8 on 2021-09-04 14:28

import corretora.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corretora', '0046_auto_20210903_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='carga',
            name='nota_fiscal_xml',
            field=models.FileField(blank=True, null=True, upload_to=corretora.models.get_file_path_notafiscal, verbose_name='NF Xml'),
        ),
        migrations.AddField(
            model_name='historicalcarga',
            name='nota_fiscal_xml',
            field=models.TextField(blank=True, max_length=100, null=True, verbose_name='NF Xml'),
        ),
    ]
