# Generated by Django 2.2.8 on 2020-10-19 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corretora', '0011_auto_20201012_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carga',
            name='veiculo',
            field=models.IntegerField(choices=[(51000, 'Rodotrem'), (39000, 'Bitrem'), (36900, 'Bicaçamba'), (36000, 'Vanderléia'), (33000, 'LS Trucada'), (25500, 'Toco')], verbose_name='Veículo'),
        ),
    ]
