# Generated by Django 2.2.16 on 2021-02-05 21:35

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_migration'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountryCodeMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', django_countries.fields.CountryField(max_length=2, unique=True)),
                ('ca_code', models.CharField(max_length=5, unique=True)),
            ],
        ),
    ]