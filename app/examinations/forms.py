from django import forms
from django.forms import inlineformset_factory
from .models import Examination, VitalSigns


class ExaminationForm(forms.ModelForm):
    class Meta:
        model = Examination
        fields = [
            'complaint', 'anamnesis', 'findings',
            'pre_diagnosis', 'diagnosis', 'icd10_code',
            'treatment_plan', 'doctor_note', 'result', 'control_date',
        ]
        widgets = {
            'complaint': forms.Textarea(attrs={'rows': 3}),
            'anamnesis': forms.Textarea(attrs={'rows': 3}),
            'findings': forms.Textarea(attrs={'rows': 3}),
            'treatment_plan': forms.Textarea(attrs={'rows': 3}),
            'doctor_note': forms.Textarea(attrs={'rows': 3}),
            'result': forms.Textarea(attrs={'rows': 3}),
            'control_date': forms.DateInput(attrs={'type': 'date'}),
        }


class VitalSignsForm(forms.ModelForm):
    class Meta:
        model = VitalSigns
        exclude = ['examination', 'bmi']
        widgets = {f: forms.NumberInput(attrs={'step': '0.1'}) for f in [
            'height', 'weight', 'temperature', 'blood_glucose'
        ]}
