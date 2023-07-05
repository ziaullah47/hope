# Generated by Django 3.2.18 on 2023-05-29 07:13

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0101_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentplan',
            name='exclude_household_error',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='paymentplan',
            name='background_action_status',
            field=django_fsm.FSMField(blank=True, choices=[('RULE_ENGINE_RUN', 'Rule Engine Running'), ('RULE_ENGINE_ERROR', 'Rule Engine Errored'), ('XLSX_EXPORTING', 'Exporting XLSX file'), ('XLSX_EXPORT_ERROR', 'Export XLSX file Error'), ('XLSX_IMPORT_ERROR', 'Import XLSX file Error'), ('XLSX_IMPORTING_ENTITLEMENTS', 'Importing Entitlements XLSX file'), ('XLSX_IMPORTING_RECONCILIATION', 'Importing Reconciliation XLSX file'), ('EXCLUDE_BENEFICIARIES', 'Exclude Beneficiaries Running'), ('EXCLUDE_BENEFICIARIES_ERROR', 'Exclude Beneficiaries Error')], db_index=True, default=None, max_length=50, null=True),
        ),
    ]