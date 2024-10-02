from django import forms
from .models import Document

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if isinstance(data, (list, tuple)):
            return [super().clean(file, initial) for file in data]
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
    # Add more fields as needed


class TestForm(forms.Form):
    test_field = forms.CharField(max_length=100, label="Test Field")



    #date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    #number_of_guest_min = forms.IntegerField(required=False, label="DINE IN")
    #number_of_guests_max = forms.IntegerField(required=False, label="DINE IN")
    #number_of_volunteers_min = forms.IntegerField(required=False, label="VOLUNTEERS")
    #number_of_volunteers_max = forms.IntegerField(required=False, label="VOLUNTEERS")
    #number_of_total_min = forms.IntegerField(required=False, label="VOLUNTEERS")
    #number_of_total_max = forms.IntegerField(required=False, label="VOLUNTEERS")
    #totalcost_min = forms.DecimalField(required=False, label="$ AMT CALC", max_digits=10, decimal_places=2)
    #totalcost_max = forms.DecimalField(required=False, label="$ AMT CALC", max_digits=10, decimal_places=2)
    #intakecost_min = forms.DecimalField(required=False, label="CASH/ CHECK COLLECTED", max_digits=10, decimal_places=2)
    #intakescripts_max = forms.DecimalField(required=False, label="CASH/ CHECK COLLECTED", max_digits=10, decimal_places=2)
    #intakescripts_min = forms.DecimalField(required=False, label="$ AMT  COLL + SCRIPTS", max_digits=10, decimal_places=2)
    #intakecost_max = forms.DecimalField(required=False, label="$ AMT  COLL + SCRIPTS", max_digits=10, decimal_places=2)
    #food_item = forms.CharField(required=False, label="Food Name", max_length=255)