# Generated by Django 2.2.8 on 2021-08-24 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corretora', '0041_auto_20210824_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpagamentofaturacargascomifrete',
            name='conta_pagadora',
            field=models.TextField(blank=True, db_index=True, max_length=200, null=True, verbose_name='Conta Pagador'),
        ),
        migrations.AlterField(
            model_name='historicalpagamentofaturacargascomifrete',
            name='fatura',
            field=models.ForeignKey(blank=True, db_constraint=False, limit_choices_to={'pagamento_fatura': False}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='corretora.FaturaCargasComiFrete'),
        ),
        migrations.AlterField(
            model_name='pagamentofaturacargascomifrete',
            name='conta_pagadora',
            field=models.TextField(blank=True, max_length=200, null=True, unique=True, verbose_name='Conta Pagador'),
        ),
        migrations.AlterField(
            model_name='pagamentofaturacargascomifrete',
            name='fatura',
            field=models.ForeignKey(limit_choices_to={'pagamento_fatura': False}, on_delete=django.db.models.deletion.PROTECT, to='corretora.FaturaCargasComiFrete'),
        ),
    ]