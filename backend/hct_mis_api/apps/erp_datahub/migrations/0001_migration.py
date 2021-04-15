# Generated by Django 2.2.8 on 2020-06-17 09:49

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('source', models.CharField(choices=[('MIS', 'HCT-MIS'), ('CA', 'Cash Assist')], max_length=3)),
                ('status', models.CharField(choices=[('NEW', 'New'), ('READY', 'Ready'), ('PROCESSING', 'Processing'), ('COMPLETED', 'Completed'), ('FAILED', 'Failed')], max_length=11)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FundsCommitment',
            fields=[
                ('business_area', models.CharField(max_length=20)),
                ('funds_commitment_number', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('document_type', models.CharField(max_length=10)),
                ('document_text', models.TextField()),
                ('currency_code', models.CharField(max_length=4, null=True)),
                ('g_l_account', models.IntegerField(null=True)),
                ('commitment_amount_local', models.DecimalField(decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('commitment_amount_usd', models.DecimalField(decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('total_open_amount_local', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('total_open_amount_usd', models.DecimalField(decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('exchange_rate', models.DecimalField(decimal_places=6, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('vendor_id', models.CharField(max_length=255, null=True)),
                ('posting_date', models.DateField(null=True)),
                ('vision_approval', models.DateField(null=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp_datahub.Session')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DownPayment',
            fields=[
                ('business_area', models.CharField(max_length=20)),
                ('down_payment_number', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('document_type', models.CharField(max_length=10)),
                ('consumer_fc_number', models.CharField(max_length=255)),
                ('total_down_payment_amount_local', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('total_down_payment_amount_usd', models.DecimalField(decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('currency_code', models.CharField(max_length=4, null=True)),
                ('exchange_rate', models.DecimalField(decimal_places=6, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('vendor_id', models.CharField(max_length=255, null=True)),
                ('posting_date', models.DateField(null=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp_datahub.Session')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]