# Generated by Django 2.2.8 on 2021-09-17 16:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('corretora', '0051_auto_20210914_2250'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalEmailsTransportadora',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('criados', models.DateTimeField(blank=True, editable=False, verbose_name='Criação')),
                ('modificado', models.DateTimeField(blank=True, editable=False, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('email', models.EmailField(blank=True, max_length=40, verbose_name='E-mail')),
                ('tipo_email', models.CharField(choices=[('notas', 'Notas Fiscais'), ('comprovantes', 'Comprovantes')], default='Notas Fiscais', max_length=12, verbose_name='Tipo')),
                ('obs', models.TextField(blank=True, max_length=2000, verbose_name='Observação')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('transp', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='corretora.Transportadora')),
            ],
            options={
                'verbose_name': 'historical Email Transportadora',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='EmailsTransportadora',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criados', models.DateTimeField(auto_now_add=True, verbose_name='Criação')),
                ('modificado', models.DateTimeField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('email', models.EmailField(blank=True, max_length=40, verbose_name='E-mail')),
                ('tipo_email', models.CharField(choices=[('notas', 'Notas Fiscais'), ('comprovantes', 'Comprovantes')], default='Notas Fiscais', max_length=12, verbose_name='Tipo')),
                ('obs', models.TextField(blank=True, max_length=2000, verbose_name='Observação')),
                ('transp', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='corretora.Transportadora')),
            ],
            options={
                'verbose_name': 'Email Transportadora',
                'verbose_name_plural': 'Emails Transportadora',
                'ordering': ['transp'],
            },
        ),
    ]
