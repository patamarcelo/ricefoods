# Generated by Django 2.2.8 on 2021-09-13 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corretora', '0049_auto_20210911_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='fornecedor',
            name='email_notafiscal_1',
            field=models.EmailField(blank=True, max_length=50, verbose_name='E-mail Nota Fiscal 1'),
        ),
        migrations.AddField(
            model_name='fornecedor',
            name='email_notafiscal_2',
            field=models.EmailField(blank=True, max_length=50, verbose_name='E-mail Nota Fiscal 2'),
        ),
        migrations.AddField(
            model_name='fornecedor',
            name='email_notafiscal_3',
            field=models.EmailField(blank=True, max_length=50, verbose_name='E-mail Nota Fiscal 3'),
        ),
        migrations.AddField(
            model_name='fornecedor',
            name='email_notafiscal_4',
            field=models.EmailField(blank=True, max_length=50, verbose_name='E-mail Nota Fiscal 4'),
        ),
        migrations.AddField(
            model_name='fornecedor',
            name='email_notafiscal_5',
            field=models.EmailField(blank=True, max_length=50, verbose_name='E-mail Nota Fiscal 5'),
        ),
        migrations.AddField(
            model_name='fornecedor',
            name='recebe_email_notafiscal',
            field=models.BooleanField(default=False, verbose_name='Recebe Nota Fiscal E-mail'),
        ),
    ]