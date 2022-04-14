# Generated by Django 3.2.12 on 2022-03-17 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0042_migration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cashplanpaymentverification',
            options={'ordering': ('created_at',)},
        ),
        migrations.AlterField(
            model_name='cashplanpaymentverification',
            name='age_filter',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='cashplanpaymentverification',
            name='excluded_admin_areas_filter',
            field=models.JSONField(null=True),
        ),
    ]