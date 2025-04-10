# forms.py
from django import forms
from .models import Diagnosis, DiagnosisUpdate,CompanySettings



class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = ['car', 'description', 'status', 'notes']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

class DiagnosisUpdateForm(forms.ModelForm):
    class Meta:
        model = DiagnosisUpdate
        fields = ['status_update', 'notes']

class CompanySettingsForm(forms.ModelForm):
    class Meta:
        model = CompanySettings
        fields = ['name', 'logo', 'address', 'vat_number', 'tel']