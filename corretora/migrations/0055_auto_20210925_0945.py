# Generated by Django 2.2.8 on 2021-09-25 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corretora', '0054_auto_20210925_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carga',
            name='obs_email_nf',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Observação Nota Fiscal'),
        ),
        migrations.AlterField(
            model_name='historicalcarga',
            name='obs_email_nf',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Observação Nota Fiscal'),
        ),
    ]
