from django import forms
from .models import Payment, Service


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['patient', 'appointment', 'examination', 'service',
                  'amount', 'discount', 'payment_type', 'payment_status', 'description']
        widgets = {
            'description': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        patient = kwargs.pop('patient', None)
        super().__init__(*args, **kwargs)
        if patient:
            from appointments.models import Appointment
            from examinations.models import Examination
            self.fields['appointment'].queryset = Appointment.objects.filter(patient=patient).order_by('-appointment_start')
            self.fields['examination'].queryset = Examination.objects.filter(patient=patient).order_by('-created_at')
        self.fields['appointment'].required = False
        self.fields['examination'].required = False
        self.fields['service'].required = False
