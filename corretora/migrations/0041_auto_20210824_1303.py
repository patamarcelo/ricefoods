# Generated by Django 2.2.8 on 2021-08-24 16:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('corretora', '0040_auto_20210824_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='faturacargascomifrete',
            name='obs',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Observação'),
        ),
        migrations.AddField(
            model_name='faturacargascomifrete',
            name='pagamento_fatura',
            field=models.BooleanField(default=False, verbose_name='Fatura Paga?'),
        ),
        migrations.AddField(
            model_name='historicalfaturacargascomifrete',
            name='obs',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Observação'),
        ),
        migrations.AddField(
            model_name='historicalfaturacargascomifrete',
            name='pagamento_fatura',
            field=models.BooleanField(default=False, verbose_name='Fatura Paga?'),
        ),
        migrations.CreateModel(
            name='PagamentoFaturaCargasComiFrete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criados', models.DateTimeField(auto_now_add=True, verbose_name='Criação')),
                ('modificado', models.DateTimeField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('data_fatura_pagamento', models.DateField(blank=True, help_text='dd/mm/aaaa', null=True, verbose_name='Data Pagamento Fatura')),
                ('valor_pago_fatura', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Valor Pago Fatura')),
                ('pagador', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Pagador')),
                ('conta_pagadora', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Conta Pagador')),
                ('obs', models.TextField(blank=True, max_length=500, verbose_name='Observação')),
                ('fatura', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='corretora.FaturaCargasComiFrete')),
            ],
            options={
                'verbose_name': 'Pagamento Fatura Terceiros',
                'verbose_name_plural': 'Pagamentos Faturas Terceiros',
            },
        ),
        migrations.CreateModel(
            name='HistoricalPagamentoFaturaCargasComiFrete',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('criados', models.DateTimeField(blank=True, editable=False, verbose_name='Criação')),
                ('modificado', models.DateTimeField(blank=True, editable=False, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('data_fatura_pagamento', models.DateField(blank=True, help_text='dd/mm/aaaa', null=True, verbose_name='Data Pagamento Fatura')),
                ('valor_pago_fatura', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Valor Pago Fatura')),
                ('pagador', models.CharField(blank=True, db_index=True, max_length=20, null=True, verbose_name='Pagador')),
                ('conta_pagadora', models.CharField(blank=True, db_index=True, max_length=20, null=True, verbose_name='Conta Pagador')),
                ('obs', models.TextField(blank=True, max_length=500, verbose_name='Observação')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('fatura', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='corretora.FaturaCargasComiFrete')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Pagamento Fatura Terceiros',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
