# Generated by Django 2.2.8 on 2020-07-12 15:42

from django.db import migrations


def remove_all(apps, schema_editor):
    SanctionListIndividual = apps.get_model(
        "sanction_list", "SanctionListIndividual"
    )
    SanctionListIndividual.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("sanction_list", "0003_migration"),
    ]

    operations = [
        migrations.RunPython(remove_all),
    ]