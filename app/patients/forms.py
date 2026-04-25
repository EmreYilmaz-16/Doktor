from django import forms
from .models import Patient, PatientMedicalInfo


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'identity_no', 'name', 'surname', 'birth_date', 'gender',
            'phone', 'email', 'address', 'blood_type',
            'emergency_contact_name', 'emergency_contact_phone',
            'insurance_info', 'occupation', 'notes', 'status',
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class PatientMedicalInfoForm(forms.ModelForm):
    class Meta:
        model = PatientMedicalInfo
        exclude = ['patient']
        widgets = {
            'allergies': forms.Textarea(attrs={'rows': 3}),
            'chronic_diseases': forms.Textarea(attrs={'rows': 3}),
            'regular_medicines': forms.Textarea(attrs={'rows': 3}),
            'surgeries': forms.Textarea(attrs={'rows': 3}),
            'family_history': forms.Textarea(attrs={'rows': 3}),
            'special_notes': forms.Textarea(attrs={'rows': 3}),
        }
