from django import forms
from .my_classes import Subject

class studentForm (forms.ModelForm):
    
    class Meta:
        model=Subject
        fields=['sub_name','sub_code']