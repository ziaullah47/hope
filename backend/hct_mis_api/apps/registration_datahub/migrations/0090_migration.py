# Generated by Django 3.2.15 on 2023-02-16 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("registration_datahub", "0089_migration"),
    ]

    operations = [
        migrations.AddField(
            model_name="importeddocumenttype",
            name="is_identity_document",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="importeddocumenttype",
            name="type",
            field=models.CharField(
                choices=[
                    ("BIRTH_CERTIFICATE", "Birth Certificate"),
                    ("DRIVERS_LICENSE", "Driver's License"),
                    ("ELECTORAL_CARD", "Electoral Card"),
                    ("NATIONAL_ID", "National ID"),
                    ("NATIONAL_PASSPORT", "National Passport"),
                    ("TAX_ID", "Tax Number Identification"),
                    ("RESIDENCE_PERMIT_NO", "Foreigner's Residence Permit"),
                    ("BANK_STATEMENT", "Bank Statement"),
                    ("OTHER", "Other"),
                ],
                max_length=50,
            ),
        ),
    ]