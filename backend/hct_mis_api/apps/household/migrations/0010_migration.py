# Generated by Django 2.2.8 on 2020-07-14 13:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0009_migration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='household',
            name='registration_date',
        ),
        migrations.AddField(
            model_name='household',
            name='first_registration_date',
            field=models.DateField(default=datetime.datetime(2020, 7, 14, 13, 42, 33, 98340)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='household',
            name='last_registration_date',
            field=models.DateField(default=datetime.datetime(2020, 7, 14, 13, 42, 42, 836944)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='individual',
            name='first_registration_date',
            field=models.DateField(default=datetime.datetime(2020, 7, 14, 13, 42, 49, 586301)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='individual',
            name='last_registration_date',
            field=models.DateField(default=datetime.datetime(2020, 7, 14, 13, 42, 54, 763979)),
            preserve_default=False,
        ),
    ]