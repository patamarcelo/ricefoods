# Generated by Django 2.2.8 on 2020-04-22 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20200422_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='projetos',
            name='link',
            field=models.TextField(choices=[('project-1', 'projeto1'), ('project-2', 'projeto2'), ('project-3', 'projeto3'), ('project-4', 'projeto4'), ('project-5', 'projeto5'), ('project-6', 'projeto6'), ('project-7', 'projeto7'), ('project-8', 'projeto8')], default=1, max_length=12, verbose_name='Area'),
            preserve_default=False,
        ),
    ]
