# Generated by Django 2.2.16 on 2021-05-24 13:28

from django.db import migrations


def round_muac(apps, schema_editor):
    Individual = apps.get_model("household", "Individual")
    individuals_with_muac = Individual.objects.filter(flex_fields__muac_i_f__isnull=False)

    for individual in individuals_with_muac:
        individual.flex_fields["muac_i_f"] = "{:.2f}".format(float(individual.flex_fields["muac_i_f"]))

    Individual.objects.bulk_update(individuals_with_muac, ("flex_fields",), 1000)


def empty_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0063_migration'),
    ]

    operations = [
        migrations.RunPython(round_muac, empty_reverse),
    ]