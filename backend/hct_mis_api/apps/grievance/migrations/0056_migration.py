# Generated by Django 3.2.15 on 2023-03-20 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grievance', '0055_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grievanceticket',
            name='household_unicef_id',
            field=models.CharField(blank=True, db_index=True, max_length=250, null=True),
        ),
    ]