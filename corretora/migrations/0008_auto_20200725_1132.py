# Generated by Django 2.2.8 on 2020-07-25 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corretora', '0007_auto_20200724_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='quantidade_pedido',
            field=models.PositiveIntegerField(help_text='Peso em Kg', verbose_name='Quantidade Pedido'),
        ),
    ]