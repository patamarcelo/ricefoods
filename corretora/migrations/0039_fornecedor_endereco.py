# Generated by Django 2.2.8 on 2021-08-24 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corretora', '0038_historicalfaturacargascomifrete'),
    ]

    operations = [
        migrations.AddField(
            model_name='fornecedor',
            name='endereco',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Endereço'),
        ),
    ]