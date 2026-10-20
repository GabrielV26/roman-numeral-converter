from django import forms

from .choices import DataTypeChoices
from .models import DataInput


class DataInputForm(forms.ModelForm):
    class Meta:
        model = DataInput
        fields = ["data_type", "value"]
        labels = {
            "data_type": "Tipo de conversão",
            "value": "Valor",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["value"].widget = forms.Textarea(attrs={
            "cols": 40,
            "rows": 3,
            "style": "width: 100%;",
            "placeholder": "Digite um número ou numeral romano",
            "maxlength": 32,
        })

    def clean_value(self):
        value = self.cleaned_data.get("value", "")
        value = value.strip()
        if not value:
            raise forms.ValidationError("Informe um valor.")
        if len(value) > 32:
            raise forms.ValidationError("O valor deve ter no máximo 32 caracteres.")
        return value
