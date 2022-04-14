# Generated by Django 2.2.16 on 2021-11-05 14:47

from django.db import migrations, models


def chunk_update(model, callback, fields):
    offset = 0
    chunk_size = 100

    while records := model.objects.all()[offset: offset + chunk_size]:
        offset += chunk_size
        for record in records:
            callback(record)

        model.objects.bulk_update(records, fields)


def assign_approved_by_to_changed_by(apps, schema_editor):
    TargetPopulation = apps.get_model('targeting', 'TargetPopulation')

    def rewrite_relation(record):
        record.changed_by = record.approved_by

    chunk_update(TargetPopulation, rewrite_relation, ["changed_by"])


def revert_assign_approved_by_to_changed_by(apps, schema_editor):
    TargetPopulation = apps.get_model('targeting', 'TargetPopulation')

    def rewrite_relation(record):
        record.approved_by = record.changed_by

    chunk_update(TargetPopulation, rewrite_relation, ["approved_by"])


class Migration(migrations.Migration):

    dependencies = [
        ('targeting', '0023_migration'),
    ]

    operations = [
        migrations.RunPython(assign_approved_by_to_changed_by, revert_assign_approved_by_to_changed_by),
    ]