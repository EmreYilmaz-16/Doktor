from django import forms
from .models import Document


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file', 'category', 'description', 'examination']
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Kısa açıklama...'}),
        }

    def __init__(self, *args, **kwargs):
        patient = kwargs.pop('patient', None)
        super().__init__(*args, **kwargs)
        if patient:
            from examinations.models import Examination
            self.fields['examination'].queryset = Examination.objects.filter(
                patient=patient
            ).order_by('-created_at')
        self.fields['examination'].required = False
