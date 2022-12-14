# Generated by Django 2.2.8 on 2020-10-28 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corretora', '0012_auto_20201019_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='produto',
            field=models.CharField(choices=[('Arroz em Casca', 'Arroz em Casca'), ('Arroz Beneficiado', 'Arroz Beneficiado'), ('Semente', 'Semente')], default='Arroz em Casca', max_length=17, verbose_name='Produto'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='tipo',
            field=models.CharField(choices=[('Saco 50Kg', 'Saco 50Kg'), ('Saco 40Kg', 'Saco 40Kg'), ('Fardo 30Kg', 'Fardo 30Kg'), ('Big Bag', 'Big Bag')], default='Saco 50Kg', max_length=12, verbose_name='Tipo'),
        ),
    ]
