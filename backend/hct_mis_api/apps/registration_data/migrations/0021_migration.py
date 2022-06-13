# Generated by Django 3.2.12 on 2022-05-17 10:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registration_data', '0020_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationdataimport',
            name='imported_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='registration_data_imports', to=settings.AUTH_USER_MODEL),
        ),
    ]