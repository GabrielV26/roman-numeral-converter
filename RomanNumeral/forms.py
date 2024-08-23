from django import forms
from .models import DataInput
from .choices import DataTypeChoices


class DataInputForm(forms.ModelForm):
    class Meta:
        model = DataInput
        fields = ['data_type', 'value']

    def __init__(self, *args, **kwargs):
        super(DataInputForm, self).__init__(*args, **kwargs)
        self.fields['value'].widget = forms.Textarea(
            attrs={
                'name': 'value',
                'cols': 40,
                'rows': 10,
                'style': 'width: 100%;',
                'required': '',
                'id': 'id_value',
                'placeholder': 'Selecione o tipo de conversão'
            }
        )

    def clean_value(self):
        data_type = self.cleaned_data.get('data_type')
        value = self.cleaned_data.get('value')
        if data_type == DataTypeChoices.TEXT:
            try:
                return value
            except ValueError:
                raise forms.ValidationError('O valor deve ser um número romano.')
        elif data_type == DataTypeChoices.FLOAT:
            try:
                return float(value)
            except ValueError:
                raise forms.ValidationError('O valor deve ser um número real.')

        return value
