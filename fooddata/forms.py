from django import forms
from .models import Document

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if isinstance(data, list):
            cleaned_files = []
            for file in data:
                cleaned_files.append(super().clean(file, initial))
            return cleaned_files
        return [super().clean(data, initial)]

class ExcelForm(forms.Form):
    files = MultipleFileField()

class AdvancedSearchExcel(forms.Form):    
    #date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    specific_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    sort_column = forms.ChoiceField(choices=[], required=False)
    lunch_item = forms.CharField(max_length=255, required=False)
    #protein = forms.CharField(max_length=255, required=False)
   
   
    # Add more fields as needed


class TestForm(forms.Form):
    test_field = forms.CharField(max_length=100, label="Test Field")



   