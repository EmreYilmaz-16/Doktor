from django import forms
from django.forms import inlineformset_factory
from .models import Prescription, PrescriptionItem


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['note', 'status']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3}),
        }


class PrescriptionItemForm(forms.ModelForm):
    class Meta:
        model = PrescriptionItem
        fields = ['medicine_name', 'active_ingredient', 'dosage', 'frequency', 'duration', 'usage_instruction', 'note']
        widgets = {
            'usage_instruction': forms.Textarea(attrs={'rows': 2}),
        }


PrescriptionItemFormSet = inlineformset_factory(
    Prescription, PrescriptionItem,
    form=PrescriptionItemForm,
    extra=3,
    can_delete=True,
    min_num=1,
    validate_min=True,
)
