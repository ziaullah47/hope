# Generated by Django 2.2.8 on 2020-08-13 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_datahub', '0015_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='importedindividual',
            name='deduplication_batch_status',
            field=models.CharField(default='UNIQUE_IN_BATCH', max_length=50),
        ),
        migrations.AddField(
            model_name='importedindividual',
            name='deduplication_golden_record_status',
            field=models.CharField(default='UNIQUE', max_length=50),
        ),
    ]