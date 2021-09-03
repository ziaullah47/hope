# Generated by Django 2.2.16 on 2021-07-08 10:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessarea',
            name='deduplication_batch_duplicate_score',
            field=models.FloatField(default=6.0, help_text='Results equal or above this score are considered duplicates', validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AddField(
            model_name='businessarea',
            name='deduplication_batch_duplicates_allowed',
            field=models.IntegerField(default=5, help_text='If amount of duplicates for single individual exceeds this limit deduplication is aborted'),
        ),
        migrations.AddField(
            model_name='businessarea',
            name='deduplication_batch_duplicates_percentage',
            field=models.IntegerField(default=50, help_text='If percentage of duplicates is higher or equal to this setting, deduplication is aborted'),
        ),
        migrations.AddField(
            model_name='businessarea',
            name='deduplication_golden_record_duplicate_score',
            field=models.FloatField(default=6.0, help_text='Results equal or above this score are considered duplicates', validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AddField(
            model_name='businessarea',
            name='deduplication_golden_record_duplicates_allowed',
            field=models.IntegerField(default=5, help_text='If amount of duplicates for single individual exceeds this limit deduplication is aborted'),
        ),
        migrations.AddField(
            model_name='businessarea',
            name='deduplication_golden_record_duplicates_percentage',
            field=models.IntegerField(default=50, help_text='If percentage of duplicates is higher or equal to this setting, deduplication is aborted'),
        ),
        migrations.AddField(
            model_name='businessarea',
            name='deduplication_golden_record_min_score',
            field=models.FloatField(default=11.0, help_text='Results below the minimum score will not be taken into account', validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]