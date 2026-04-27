from django import forms
from django.forms import inlineformset_factory
from .models import Prescription, PrescriptionItem


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['note']
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Zorunlu olmayan alanları opsiyonel yap
        self.fields['frequency'].required = False
        self.fields['dosage'].required = False


PrescriptionItemFormSet = inlineformset_factory(
    Prescription, PrescriptionItem,
    form=PrescriptionItemForm,
    extra=0,
    can_delete=True,
    min_num=0,
    validate_min=False,
)
