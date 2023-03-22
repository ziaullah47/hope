# Generated by Django 3.2.15 on 2023-03-10 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0137_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documenttype',
            name='type',
            field=models.CharField(choices=[('BIRTH_CERTIFICATE', 'Birth Certificate'), ('DRIVERS_LICENSE', "Driver's License"), ('ELECTORAL_CARD', 'Electoral Card'), ('NATIONAL_ID', 'National ID'), ('NATIONAL_PASSPORT', 'National Passport'), ('TAX_ID', 'Tax Number Identification'), ('RESIDENCE_PERMIT_NO', "Foreigner's Residence Permit"), ('BANK_STATEMENT', 'Bank Statement'), ('DISABILITY_CERTIFICATE', 'Disability Certificate'), ('OTHER', 'Other')], max_length=50, unique=True),
        ),
    ]