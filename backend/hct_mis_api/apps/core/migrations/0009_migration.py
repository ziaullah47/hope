# Generated by Django 2.2.16 on 2021-01-22 00:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_migration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='businessarea',
            old_name='kobo_token',
            new_name='kobo_username',
        ),
    ]