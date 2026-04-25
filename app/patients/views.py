from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404

from core.mixins import create_audit_log
from .models import Patient, PatientMedicalInfo
from .forms import PatientForm, PatientMedicalInfoForm


class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'patients/list.html'
    context_object_name = 'patients'
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(surname__icontains=q) |
                Q(phone__icontains=q) |
                Q(identity_no__icontains=q)
            )
        status = self.request.GET.get('status', '')
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        ctx['status_filter'] = self.request.GET.get('status', '')
        return ctx


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'patients/detail.html'
    context_object_name = 'patient'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        create_audit_log(
            self.request, 'VIEW', 'Patient', obj.pk,
            f'Hasta kartı görüntülendi: {obj.full_name}'
        )
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        patient = self.object
        ctx['appointments'] = patient.appointments.select_related('doctor__user').order_by('-appointment_start')[:10]
        ctx['examinations'] = patient.examinations.select_related('doctor__user').order_by('-created_at')[:10]
        ctx['prescriptions'] = patient.prescriptions.order_by('-created_at')[:10]
        ctx['documents'] = patient.documents.order_by('-created_at')[:10]
        ctx['payments'] = patient.payments.order_by('-created_at')[:10]
        try:
            ctx['medical_info'] = patient.medical_info
        except PatientMedicalInfo.DoesNotExist:
            ctx['medical_info'] = None
        return ctx


class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/form.html'

    def get_success_url(self):
        return reverse_lazy('patients:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        # Tıbbi bilgi kaydı oluştur
        PatientMedicalInfo.objects.get_or_create(patient=self.object)
        create_audit_log(
            self.request, 'CREATE', 'Patient', self.object.pk,
            f'Yeni hasta kaydı: {self.object.full_name}'
        )
        messages.success(self.request, f'{self.object.full_name} başarıyla kaydedildi.')
        return response


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/form.html'

    def get_success_url(self):
        return reverse_lazy('patients:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        create_audit_log(
            self.request, 'UPDATE', 'Patient', self.object.pk,
            f'Hasta güncellendi: {self.object.full_name}'
        )
        messages.success(self.request, 'Hasta bilgileri güncellendi.')
        return response


class PatientMedicalInfoUpdateView(LoginRequiredMixin, UpdateView):
    model = PatientMedicalInfo
    form_class = PatientMedicalInfoForm
    template_name = 'patients/medical_form.html'

    def get_object(self, queryset=None):
        patient = get_object_or_404(Patient, pk=self.kwargs['patient_pk'])
        obj, _ = PatientMedicalInfo.objects.get_or_create(patient=patient)
        return obj

    def get_success_url(self):
        return reverse_lazy('patients:detail', kwargs={'pk': self.kwargs['patient_pk']})

    def form_valid(self, form):
        messages.success(self.request, 'Sağlık bilgileri güncellendi.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['patient'] = get_object_or_404(Patient, pk=self.kwargs['patient_pk'])
        return ctx
