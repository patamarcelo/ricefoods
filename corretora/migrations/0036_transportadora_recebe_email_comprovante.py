# Generated by Django 2.2.8 on 2021-08-23 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corretora', '0035_auto_20210823_0821'),
    ]

    operations = [
        migrations.AddField(
            model_name='transportadora',
            name='recebe_email_comprovante',
            field=models.BooleanField(default=False, verbose_name='Recebe Comprovante E-mail'),
        ),
    ]
