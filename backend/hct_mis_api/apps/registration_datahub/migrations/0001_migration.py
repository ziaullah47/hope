# Generated by Django 2.2.8 on 2020-04-29 08:18

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import model_utils.fields
import phonenumber_field.modelfields
import sorl.thumbnail.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('label', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ImportData',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('xlsx_file', models.FileField(upload_to='')),
                ('number_of_households', models.PositiveIntegerField()),
                ('number_of_individuals', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ImportedDocumentType',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('label', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ImportedHousehold',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('consent', sorl.thumbnail.fields.ImageField(upload_to='', validators=[django.core.validators.validate_image_file_extension])),
                ('residence_status', models.CharField(choices=[('REFUGEE', 'Refugee'), ('MIGRANT', 'Migrant'), ('CITIZEN', 'Citizen'), ('IDP', 'IDP'), ('OTHER', 'Other')], max_length=255)),
                ('country_origin', django_countries.fields.CountryField(max_length=2)),
                ('size', models.PositiveIntegerField()),
                ('address', models.CharField(blank=True, max_length=255)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('admin1', models.CharField(blank=True, max_length=255)),
                ('admin2', models.CharField(blank=True, max_length=255)),
                ('geopoint', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('female_age_group_0_5_count', models.PositiveIntegerField(default=0)),
                ('female_age_group_6_11_count', models.PositiveIntegerField(default=0)),
                ('female_age_group_12_17_count', models.PositiveIntegerField(default=0)),
                ('female_adults_count', models.PositiveIntegerField(default=0)),
                ('pregnant_count', models.PositiveIntegerField(default=0)),
                ('male_age_group_0_5_count', models.PositiveIntegerField(default=0)),
                ('male_age_group_6_11_count', models.PositiveIntegerField(default=0)),
                ('male_age_group_12_17_count', models.PositiveIntegerField(default=0)),
                ('male_adults_count', models.PositiveIntegerField(default=0)),
                ('female_age_group_0_5_disabled_count', models.PositiveIntegerField(default=0)),
                ('female_age_group_6_11_disabled_count', models.PositiveIntegerField(default=0)),
                ('female_age_group_12_17_disabled_count', models.PositiveIntegerField(default=0)),
                ('female_adults_disabled_count', models.PositiveIntegerField(default=0)),
                ('male_age_group_0_5_disabled_count', models.PositiveIntegerField(default=0)),
                ('male_age_group_6_11_disabled_count', models.PositiveIntegerField(default=0)),
                ('male_age_group_12_17_disabled_count', models.PositiveIntegerField(default=0)),
                ('male_adults_disabled_count', models.PositiveIntegerField(default=0)),
                ('registration_date', models.DateField(null=True)),
                ('returnee', models.BooleanField(default=False, null=True)),
                ('flex_fields', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ImportedIndividual',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('individual_id', models.CharField(blank=True, max_length=255)),
                ('photo', models.ImageField(blank=True, upload_to='')),
                ('full_name', models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(255)])),
                ('given_name', models.CharField(blank=True, max_length=85)),
                ('middle_name', models.CharField(blank=True, max_length=85)),
                ('family_name', models.CharField(blank=True, max_length=85)),
                ('relationship', models.CharField(blank=True, choices=[('NON_BENEFICIARY', 'Not a Family Member. Can only act as a recipient.'), ('HEAD', 'Head of household (self)'), ('SON_DAUGHTER', 'Son / Daughter'), ('WIFE_HUSBAND', 'Wife / Husband'), ('BROTHER_SISTER', 'Brother / Sister'), ('MOTHER_FATHER', 'Mother / Father'), ('AUNT_UNCLE', 'Aunt / Uncle'), ('GRANDMOTHER_GRANDFATHER', 'Grandmother / Grandfather'), ('MOTHERINLAW_FATHERINLAW', 'Mother-in-law / Father-in-law'), ('DAUGHTERINLAW_SONINLAW', 'Daughter-in-law / Son-in-law'), ('SISTERINLAW_BROTHERINLAW', 'Sister-in-law / Brother-in-law'), ('GRANDDAUGHER_GRANDSON', 'Granddaughter / Grandson'), ('NEPHEW_NIECE', 'Nephew / Niece'), ('COUSIN', 'Cousin')], max_length=255)),
                ('role', models.CharField(blank=True, choices=[('PRIMARY', 'Primary collector'), ('ALTERNATE', 'Alternate collector'), ('NO_ROLE', 'None')], max_length=255)),
                ('sex', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')], max_length=255)),
                ('birth_date', models.DateField()),
                ('estimated_birth_date', models.BooleanField(default=False, null=True)),
                ('marital_status', models.CharField(choices=[('SINGLE', 'SINGLE'), ('MARRIED', 'Married'), ('WIDOW', 'Widow'), ('DIVORCED', 'Divorced'), ('SEPARATED', 'Separated')], max_length=255)),
                ('phone_no', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('phone_no_alternative', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('disability', models.BooleanField(default=False)),
                ('flex_fields', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('household', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='individuals', to='registration_datahub.ImportedHousehold')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegistrationDataImportDatahub',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('import_date', models.DateTimeField(auto_now_add=True)),
                ('hct_id', models.UUIDField(null=True)),
                ('import_data', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='registration_data_import', to='registration_datahub.ImportData')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ImportedIndividualIdentity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_number', models.CharField(max_length=255)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='identities', to='registration_datahub.Agency')),
                ('individual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='identities', to='registration_datahub.ImportedIndividual')),
            ],
        ),
        migrations.AddField(
            model_name='importedindividual',
            name='registration_data_import',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='individuals', to='registration_datahub.RegistrationDataImportDatahub'),
        ),
        migrations.CreateModel(
            name='ImportedHouseholdIdentity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_number', models.CharField(max_length=255)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='households_identities', to='registration_datahub.Agency')),
                ('household', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='identities', to='registration_datahub.ImportedHousehold')),
            ],
        ),
        migrations.AddField(
            model_name='importedhousehold',
            name='head_of_household',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='registration_datahub.ImportedIndividual'),
        ),
        migrations.AddField(
            model_name='importedhousehold',
            name='registration_data_import',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='households', to='registration_datahub.RegistrationDataImportDatahub'),
        ),
        migrations.CreateModel(
            name='ImportedDocument',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('document_number', models.CharField(blank=True, max_length=255)),
                ('photo', models.ImageField(blank=True, upload_to='')),
                ('individual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='registration_datahub.ImportedIndividual')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='registration_datahub.ImportedDocumentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DocumentValidator',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('regex', models.CharField(default='.*', max_length=100)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='validators', to='registration_datahub.ImportedDocumentType')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]