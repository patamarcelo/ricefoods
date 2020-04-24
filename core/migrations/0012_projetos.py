# Generated by Django 2.2.8 on 2020-04-22 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20200421_1145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Projetos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criados', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo ?')),
                ('titulo', models.CharField(max_length=100, verbose_name='Título')),
                ('subtitulo', models.CharField(max_length=100, verbose_name='Subtítulo')),
                ('descricao', models.TextField(max_length=250, verbose_name='Descrição')),
                ('area', models.TextField(choices=[('originacao', 'Originação'), ('abast', 'Abastecimento'), ('impexp', 'Importação e Exportação'), ('logistica', 'Logística')], max_length=12, verbose_name='Area')),
                ('area2', models.TextField(choices=[('originacao', 'Originação'), ('abast', 'Abastecimento'), ('impexp', 'Importação e Exportação'), ('logistica', 'Logística')], max_length=12, verbose_name='Area2')),
            ],
            options={
                'verbose_name': 'Projeto',
                'verbose_name_plural': 'Projetos',
            },
        ),
    ]
