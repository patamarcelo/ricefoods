# Generated by Django 2.2.8 on 2020-06-24 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corretora', '0002_auto_20200624_0747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carga',
            name='vpcomissaoc',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7, verbose_name='Valor Comissao'),
        ),
        migrations.AlterField(
            model_name='carga',
            name='vpcomissaof',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7, verbose_name='Valor Comissao F'),
        ),
    ]
