# Generated by Django 2.2.16 on 2021-02-10 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0047_migration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='household',
            old_name='deactivated',
            new_name='withdrawn',
        ),
        migrations.RenameField(
            model_name='household',
            old_name='deactivated_date',
            new_name='withdrawn_date',
        ),
    ]