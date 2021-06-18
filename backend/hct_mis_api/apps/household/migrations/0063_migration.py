# Generated by Django 2.2.16 on 2021-05-04 11:57
from itertools import zip_longest

from django.db import migrations


def cast_single_flex_field(value):
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    return str(value)


def cast_flex_fields(flex_fields, flex_attrs_name_list):
    for key, value in flex_fields.items():
        if key not in flex_attrs_name_list:
            continue
        flex_fields[key] = cast_single_flex_field(value)


def cast_flex_field_values(apps, schema_editor):
    Individual = apps.get_model("household", "Individual")
    Household = apps.get_model("household", "Household")
    FlexibleAttribute = apps.get_model("core", "FlexibleAttribute")
    flex_attrs_name_list = FlexibleAttribute.objects.filter(type="SELECT_ONE").values_list("name", flat=True)
    individuals = Individual.objects.all()
    households = Household.objects.all()
    for individual, household in zip_longest(individuals, households):
        if individual is not None:
            cast_flex_fields(individual.flex_fields, flex_attrs_name_list)
        if household is not None:
            cast_flex_fields(household.flex_fields, flex_attrs_name_list)

    Individual.objects.bulk_update(individuals, ("flex_fields",))
    Household.objects.bulk_update(households, ("flex_fields",))


def empty_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("household", "0062_migration"),
    ]

    operations = [
        migrations.RunPython(cast_flex_field_values, empty_reverse),
    ]