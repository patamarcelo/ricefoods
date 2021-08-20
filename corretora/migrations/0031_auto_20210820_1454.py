# Generated by Django 2.2.8 on 2021-08-20 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corretora', '0030_auto_20210820_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='carga',
            name='comi_frete_total',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Valor Total', max_digits=5, null=True, verbose_name='Comi F Total'),
        ),
        migrations.AddField(
            model_name='historicalcarga',
            name='comi_frete_total',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Valor Total', max_digits=5, null=True, verbose_name='Comi F Total'),
        ),
        migrations.AlterField(
            model_name='carga',
            name='comi_frete_ton',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Valor por tonelada', max_digits=5, null=True, verbose_name='Comi Frete'),
        ),
        migrations.AlterField(
            model_name='carga',
            name='gera_comi_frete',
            field=models.BooleanField(default=False, verbose_name='Comi Frete'),
        ),
        migrations.AlterField(
            model_name='historicalcarga',
            name='comi_frete_ton',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Valor por tonelada', max_digits=5, null=True, verbose_name='Comi Frete'),
        ),
        migrations.AlterField(
            model_name='historicalcarga',
            name='gera_comi_frete',
            field=models.BooleanField(default=False, verbose_name='Comi Frete'),
        ),
    ]
