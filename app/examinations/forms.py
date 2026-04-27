from django import forms
from django.forms import inlineformset_factory
from appointments.models import Doctor
from .models import Examination, VitalSigns, ExaminationTemplate


class ExaminationForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.filter(status=True).select_related('user'),
        required=False,
        label='Doktor',
        help_text='Sadece doktor olmayan kullanıcılar için gereklidir.',
    )

    class Meta:
        model = Examination
        fields = [
            'doctor',
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

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        # Doktor olan kullanıcılar için doktor alanını gizle
        if user and hasattr(user, 'doctor_profile'):
            self.fields['doctor'].widget = forms.HiddenInput()
            self.fields['doctor'].required = False
        else:
            self.fields['doctor'].required = True


class VitalSignsForm(forms.ModelForm):
    class Meta:
        model = VitalSigns
        exclude = ['examination', 'bmi']
        widgets = {f: forms.NumberInput(attrs={'step': '0.1'}) for f in [
            'height', 'weight', 'temperature', 'blood_glucose'
        ]}


class ExaminationTemplateForm(forms.ModelForm):
    class Meta:
        model = ExaminationTemplate
        fields = ['name', 'category', 'complaint', 'findings', 'diagnosis',
                  'icd10_code', 'treatment_plan', 'doctor_note', 'is_shared']
        widgets = {
            'complaint':      forms.Textarea(attrs={'rows': 3}),
            'findings':       forms.Textarea(attrs={'rows': 3}),
            'treatment_plan': forms.Textarea(attrs={'rows': 3}),
            'doctor_note':    forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name':           'Şablon Adı',
            'category':       'Kategori',
            'complaint':      'Şikayet',
            'findings':       'Fizik Muayene Bulguları',
            'diagnosis':      'Tanı',
            'icd10_code':     'ICD-10 Kodu',
            'treatment_plan': 'Tedavi Planı',
            'doctor_note':    'Doktor Notu',
            'is_shared':      'Herkese açık şablon',
        }
