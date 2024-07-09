# Generated by Django 3.2.25 on 2024-06-04 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0131_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='transaction_reference_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='transaction_status_blockchain_link',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='paymentrecord',
            name='transaction_reference_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='paymentrecord',
            name='transaction_status_blockchain_link',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]