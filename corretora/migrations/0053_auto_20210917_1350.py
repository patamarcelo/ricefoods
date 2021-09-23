# Generated by Django 2.2.8 on 2021-09-17 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corretora', '0052_emailstransportadora_historicalemailstransportadora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailstransportadora',
            name='tipo_email',
            field=models.CharField(choices=[('notas', 'Notas Fiscais'), ('comprovantes', 'Comprovantes')], max_length=12, verbose_name='Tipo'),
        ),
        migrations.AlterField(
            model_name='historicalemailstransportadora',
            name='tipo_email',
            field=models.CharField(choices=[('notas', 'Notas Fiscais'), ('comprovantes', 'Comprovantes')], max_length=12, verbose_name='Tipo'),
        ),
    ]