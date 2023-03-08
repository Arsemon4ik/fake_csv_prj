from django import forms
from django.forms import ModelForm, inlineformset_factory
from .models import Column, Schema


class SchemaForm(ModelForm):
    class Meta:
        model = Schema
        fields = ('title', 'column_separator', 'string_character')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'


class ColumnForm(ModelForm):
    class Meta:
        model = Column
        fields = ("column_name", "column_type", "from_range", "to_range", "order")
        widgets = {
            'column_name': forms.TextInput(attrs={'class': 'form-control'},),
            'column_type': forms.Select(attrs={'class': 'form-control'}),
            'from_range': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'to_range': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '100'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

        # make fields required based on model
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for bound_field in self:
                if hasattr(bound_field, "field") and bound_field.field.required:
                    bound_field.field.widget.attrs["required"] = "required"


ColumnFormSet = inlineformset_factory(
    parent_model=Schema, model=Column, form=ColumnForm,
    extra=1, can_delete=True, can_delete_extra=True
)

