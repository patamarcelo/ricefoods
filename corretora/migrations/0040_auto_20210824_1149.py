# Generated by Django 2.2.8 on 2021-08-24 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corretora', '0039_fornecedor_endereco'),
    ]

    operations = [
        migrations.AddField(
            model_name='faturacargascomifrete',
            name='enviada_cobranca',
            field=models.BooleanField(default=False, verbose_name='Enviada Cobrança?'),
        ),
        migrations.AddField(
            model_name='historicalfaturacargascomifrete',
            name='enviada_cobranca',
            field=models.BooleanField(default=False, verbose_name='Enviada Cobrança?'),
        ),
    ]
