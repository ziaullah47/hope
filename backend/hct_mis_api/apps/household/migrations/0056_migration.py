# Generated by Django 2.2.16 on 2021-02-23 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0055_migration'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='document',
            name='unique_if_not_removed',
        ),
        migrations.AddField(
            model_name='document',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('VALID', 'Valid'), ('INVALID', 'Invalid')], default='VALID', max_length=20),
        ),
        migrations.AddConstraint(
            model_name='document',
            constraint=models.UniqueConstraint(condition=models.Q(models.Q(('is_removed', False), ('status', 'VALID'))), fields=('document_number', 'type'), name='unique_if_not_removed_and_valid'),
        ),
    ]