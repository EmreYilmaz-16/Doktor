from django import forms
from .models import Appointment, Doctor


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'appointment_start', 'appointment_end',
                  'appointment_type', 'status', 'note']
        widgets = {
            'appointment_start': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'appointment_end': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'note': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['appointment_start'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['appointment_end'].input_formats = ['%Y-%m-%dT%H:%M']
        from patients.models import Patient
        self.fields['patient'].queryset = Patient.objects.filter(status='ACTIVE').order_by('surname', 'name')
        self.fields['doctor'].queryset = Doctor.objects.filter(status=True).select_related('user')

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('appointment_start')
        end = cleaned.get('appointment_end')
        doctor = cleaned.get('doctor')
        if start and end:
            if end <= start:
                raise forms.ValidationError('Bitiş zamanı başlangıç zamanından sonra olmalıdır.')
            # Çakışma kontrolü
            if doctor:
                qs = Appointment.objects.filter(
                    doctor=doctor,
                    appointment_start__lt=end,
                    appointment_end__gt=start,
                ).exclude(status__in=['CANCELLED', 'NO_SHOW'])
                if self.instance.pk:
                    qs = qs.exclude(pk=self.instance.pk)
                if qs.exists():
                    raise forms.ValidationError('Bu doktorun seçilen saatte başka bir randevusu var.')
        return cleaned
