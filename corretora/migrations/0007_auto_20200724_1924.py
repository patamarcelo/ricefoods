# Generated by Django 2.2.8 on 2020-07-24 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corretora', '0006_auto_20200713_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carga',
            name='veiculo',
            field=models.IntegerField(choices=[(51000, 'Rodotrem'), (39000, 'Bitrem'), (37000, 'Bicaçamba'), (36000, 'Vanderléia'), (32000, 'LS Trucada'), (26000, 'Toco')], verbose_name='Veículo'),
        ),
    ]