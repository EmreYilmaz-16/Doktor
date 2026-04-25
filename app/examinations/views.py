from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404

from core.mixins import create_audit_log, DoctorRequiredMixin
from patients.models import Patient
from appointments.models import Appointment, AppointmentStatus
from .models import Examination, VitalSigns
from .forms import ExaminationForm, VitalSignsForm


class ExaminationCreateView(LoginRequiredMixin, DoctorRequiredMixin, CreateView):
    model = Examination
    form_class = ExaminationForm
    template_name = 'examinations/form.html'

    def dispatch(self, request, *args, **kwargs):
        self.patient = get_object_or_404(Patient, pk=kwargs['patient_pk'])
        self.appointment = None
        apt_pk = kwargs.get('appointment_pk')
        if apt_pk:
            self.appointment = get_object_or_404(Appointment, pk=apt_pk)
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        self.vitals_form = VitalSignsForm(
            self.request.POST or None,
            prefix='vitals'
        )
        return form

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['patient'] = self.patient
        ctx['appointment'] = self.appointment
        ctx['vitals_form'] = self.vitals_form
        ctx['past_examinations'] = self.patient.examinations.select_related('doctor__user').order_by('-created_at')[:5]
        return ctx

    def form_valid(self, form):
        if not self.vitals_form.is_valid():
            return self.form_invalid(form)

        form.instance.patient = self.patient
        try:
            form.instance.doctor = self.request.user.doctor_profile
        except Exception:
            messages.error(self.request, 'Doktor profili bulunamadı.')
            return self.form_invalid(form)

        if self.appointment:
            form.instance.appointment = self.appointment

        response = super().form_valid(form)

        vitals = self.vitals_form.save(commit=False)
        vitals.examination = self.object
        vitals.save()

        if self.appointment:
            self.appointment.status = AppointmentStatus.COMPLETED
            self.appointment.save(update_fields=['status', 'updated_at'])

        create_audit_log(
            self.request, 'CREATE', 'Examination', self.object.pk,
            f'Muayene kaydı: {self.patient.full_name}'
        )
        messages.success(self.request, 'Muayene kaydı oluşturuldu.')
        return response

    def get_success_url(self):
        return reverse_lazy('examinations:detail', kwargs={'pk': self.object.pk})


class ExaminationDetailView(LoginRequiredMixin, DetailView):
    model = Examination
    template_name = 'examinations/detail.html'
    context_object_name = 'examination'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        create_audit_log(
            self.request, 'VIEW', 'Examination', obj.pk,
            f'Muayene görüntülendi: {obj.patient.full_name}'
        )
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        try:
            ctx['vitals'] = self.object.vitals
        except VitalSigns.DoesNotExist:
            ctx['vitals'] = None
        ctx['prescriptions'] = self.object.prescriptions.prefetch_related('items').all()
        ctx['documents'] = self.object.documents.all()
        return ctx


class ExaminationUpdateView(LoginRequiredMixin, DoctorRequiredMixin, UpdateView):
    model = Examination
    form_class = ExaminationForm
    template_name = 'examinations/form.html'

    def get_success_url(self):
        return reverse_lazy('examinations:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['patient'] = self.object.patient
        ctx['vitals_form'] = VitalSignsForm(
            self.request.POST or None,
            instance=getattr(self.object, 'vitals', None),
            prefix='vitals'
        )
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        vitals_form = ctx['vitals_form']
        if vitals_form.is_valid():
            vitals = vitals_form.save(commit=False)
            vitals.examination = self.object
            vitals.save()
        messages.success(self.request, 'Muayene güncellendi.')
        return super().form_valid(form)
