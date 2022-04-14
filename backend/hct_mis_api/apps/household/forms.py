from typing import Optional

from django import forms
from django.core.exceptions import ValidationError

from hct_mis_api.apps.core.models import BusinessArea
from hct_mis_api.apps.household.models import XlsxUpdateFile
from hct_mis_api.apps.registration_data.models import RegistrationDataImport


class UpdateByXlsxStage1Form(forms.Form):
    business_area = forms.ModelChoiceField(queryset=BusinessArea.objects.all())
    registration_data_import = forms.ModelChoiceField(queryset=RegistrationDataImport.objects.all())
    file = forms.FileField()

    def clean_registration_data_import(self) -> Optional[RegistrationDataImport]:
        data = self.cleaned_data.get("registration_data_import")

        if not data:
            return None

        registration_data_import = self._retrieve_rdi_by_name()

        self._check_rdi_has_correct_business_area(registration_data_import)

        return registration_data_import

    def _check_rdi_has_correct_business_area(self, registration_data_import) -> None:
        business_area = self.cleaned_data.get("business_area")
        if registration_data_import.business_area != business_area:
            raise ValidationError("Rdi should belong to selected business area")

    def _retrieve_rdi_by_name(self) -> RegistrationDataImport:
        data = self.cleaned_data.get("registration_data_import")
        registration_data_import = RegistrationDataImport.objects.filter(name=data).first()
        if not registration_data_import:
            raise ValidationError(f"Rdi with the name {data} doesn't exist")
        return registration_data_import


class UpdateByXlsxStage2Form(forms.Form):
    xlsx_update_file = forms.ModelChoiceField(queryset=XlsxUpdateFile.objects.all(), widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.xlsx_columns = kwargs.pop("xlsx_columns", [])
        super().__init__(*args, **kwargs)
        self.fields["xlsx_match_columns"] = forms.MultipleChoiceField(
            widget=forms.CheckboxSelectMultiple,
            choices=[(xlsx_column, xlsx_column) for xlsx_column in self.xlsx_columns],
        )

    def clean_xlsx_match_columns(self):
        data = self.cleaned_data["xlsx_match_columns"]
        required_columns = {"individual__unicef_id", "household__unicef_id"}
        all_columns = set(self.xlsx_columns)
        required_columns_in_this_form = all_columns & required_columns
        columns_not_found = required_columns_in_this_form - set(data)
        if not len(columns_not_found):
            return data
        raise ValidationError("Unicef Id columns have to be selected")