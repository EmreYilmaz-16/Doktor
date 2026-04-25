from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from core.mixins import create_audit_log, DoctorRequiredMixin
from examinations.models import Examination
from .models import Prescription, PrescriptionItem
from .forms import PrescriptionForm, PrescriptionItemFormSet
from .pdf import generate_prescription_pdf


class PrescriptionCreateView(LoginRequiredMixin, DoctorRequiredMixin, CreateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'prescriptions/form.html'

    def dispatch(self, request, *args, **kwargs):
        self.examination = get_object_or_404(Examination, pk=kwargs['examination_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['examination'] = self.examination
        ctx['patient'] = self.examination.patient
        ctx['item_formset'] = PrescriptionItemFormSet(self.request.POST or None)
        # Alerji uyarısı
        try:
            ctx['allergies'] = self.examination.patient.medical_info.allergies
        except Exception:
            ctx['allergies'] = ''
        return ctx

    def form_valid(self, form):
        item_formset = PrescriptionItemFormSet(self.request.POST)
        if not item_formset.is_valid():
            return self.form_invalid(form)

        form.instance.examination = self.examination
        form.instance.patient = self.examination.patient
        form.instance.doctor = self.examination.doctor
        response = super().form_valid(form)
        item_formset.instance = self.object
        item_formset.save()

        create_audit_log(
            self.request, 'CREATE', 'Prescription', self.object.pk,
            f'Reçete oluşturuldu: {self.examination.patient.full_name}'
        )
        messages.success(self.request, 'Reçete oluşturuldu.')
        return response

    def get_success_url(self):
        return reverse_lazy('prescriptions:detail', kwargs={'pk': self.object.pk})


class PrescriptionDetailView(LoginRequiredMixin, DetailView):
    model = Prescription
    template_name = 'prescriptions/detail.html'
    context_object_name = 'prescription'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['items'] = self.object.items.all()
        return ctx


class PrescriptionPdfView(LoginRequiredMixin, DetailView):
    model = Prescription

    def get(self, request, *args, **kwargs):
        prescription = self.get_object()
        create_audit_log(
            request, 'PRINT', 'Prescription', prescription.pk,
            f'Reçete PDF: {prescription.patient.full_name}'
        )
        pdf_bytes = generate_prescription_pdf(prescription)
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="recete_{prescription.pk}.pdf"'
        return response
