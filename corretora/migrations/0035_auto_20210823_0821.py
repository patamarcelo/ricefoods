# Generated by Django 2.2.8 on 2021-08-23 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corretora', '0034_auto_20210822_0952'),
    ]

    operations = [
        migrations.AddField(
            model_name='carga',
            name='obs_descarga',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Observação Descarga'),
        ),
        migrations.AddField(
            model_name='historicalcarga',
            name='obs_descarga',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Observação Descarga'),
        ),
    ]
