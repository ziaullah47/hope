# Generated by Django 2.2.16 on 2021-01-12 15:40

import concurrency.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0018_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashplanpaymentverification',
            name='version',
            field=concurrency.fields.IntegerVersionField(default=0, help_text='record revision number'),
        ),
    ]