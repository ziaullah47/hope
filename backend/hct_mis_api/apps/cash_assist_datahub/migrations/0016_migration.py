# Generated by Django 3.2.19 on 2023-07-27 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cash_assist_datahub', '0001_migration_squashed_0015_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='business_area',
            field=models.CharField(help_text='Same as the business area set on program, but\n            this is set as the same value, and all other\n            models this way can get easy access to the business area\n            via the session.', max_length=20),
        ),
    ]
