# Generated by Django 3.2.12 on 2022-03-18 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('steficon', '0014_migration'),
        ('targeting', '0031_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rule',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]