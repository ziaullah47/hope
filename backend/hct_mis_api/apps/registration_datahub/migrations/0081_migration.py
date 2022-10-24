# Generated by Django 3.2.15 on 2022-10-03 17:56

from django.db import migrations

from hct_mis_api.apps.household.models import IDENTIFICATION_TYPE_CHOICE


def migrate_doc_type(apps, schema_editor):
    ImportedDocument = apps.get_model('registration_datahub', 'ImportedDocument')
    ImportedDocumentType = apps.get_model('registration_datahub', 'ImportedDocumentType')

    countries = ImportedDocumentType.objects.order_by('country').values_list('country', flat=True).distinct()

    for country in countries:
        ImportedDocument.objects.filter(type__country=country).update(country=country)

    tostay = countries.first()
    if tostay:
        for code, _ in IDENTIFICATION_TYPE_CHOICE:
            new_type, _ = ImportedDocumentType.objects.get_or_create(type=code, country=tostay)
            ImportedDocument.objects.filter(type__type=code).update(type=new_type)
        ImportedDocumentType.objects.exclude(country=tostay).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('registration_datahub', '0080_migration'),
    ]

    operations = [
        migrations.RunPython(migrate_doc_type, migrations.RunPython.noop),
    ]