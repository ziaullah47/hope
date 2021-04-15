# Generated by Django 2.2.16 on 2020-12-24 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mis_datahub', '0025_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='household',
            name='residence_status',
            field=models.CharField(choices=[('', 'None'), ('IDP', 'Displaced  |  Internally Displaced People'), ('REFUGEE', 'Displaced  |  Refugee / Asylum Seeker'), ('OTHERS_OF_CONCERN', 'Displaced  |  Others of Concern'), ('HOST', 'Non-displaced  |   Host'), ('NON_HOST', 'Non-displaced  |   Non-host')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='individual',
            name='marital_status',
            field=models.CharField(choices=[('', 'None'), ('SINGLE', 'Single'), ('MARRIED', 'Married'), ('WIDOWED', 'Widowed'), ('DIVORCED', 'Divorced'), ('SEPARATED', 'Separated')], max_length=255),
        ),
    ]