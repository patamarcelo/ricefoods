# Generated by Django 2.2.8 on 2021-02-02 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corretora', '0023_datasemcarga_historicaldatasemcarga'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='descarga_sabado',
            field=models.BooleanField(default=False, verbose_name='Descarga Sábado'),
        ),
        migrations.AlterField(
            model_name='datasemcarga',
            name='obs',
            field=models.TextField(blank=True, max_length=2000, verbose_name='Observação'),
        ),
        migrations.AlterField(
            model_name='historicaldatasemcarga',
            name='obs',
            field=models.TextField(blank=True, max_length=2000, verbose_name='Observação'),
        ),
    ]
