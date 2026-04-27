from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q

from core.mixins import create_audit_log
from examinations.models import Examination
from .models import Prescription, PrescriptionItem
from .forms import PrescriptionForm, PrescriptionItemFormSet
from .pdf import generate_prescription_pdf


class PrescriptionCreateView(LoginRequiredMixin, CreateView):
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
            messages.error(self.request, f'İlaç bilgilerinde hata: {item_formset.errors}')
            return self.form_invalid(form)

        # En az 1 ilaç girilmeli
        has_items = any(
            f.cleaned_data.get('medicine_name') and not f.cleaned_data.get('DELETE', False)
            for f in item_formset.forms
        )
        if not has_items:
            messages.error(self.request, 'En az bir ilaç eklemelisiniz.')
            return self.form_invalid(form)

        form.instance.examination = self.examination
        form.instance.patient = self.examination.patient
        form.instance.doctor = self.examination.doctor
        form.instance.status = 'ACTIVE'
        self.object = form.save()
        item_formset.instance = self.object
        item_formset.save()

        create_audit_log(
            self.request, 'CREATE', 'Prescription', self.object.pk,
            f'Reçete oluşturuldu: {self.examination.patient.full_name}'
        )
        messages.success(self.request, 'Reçete oluşturuldu.')
        from django.shortcuts import redirect
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('prescriptions:detail', kwargs={'pk': self.object.pk})


class PrescriptionUpdateView(LoginRequiredMixin, UpdateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'prescriptions/form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['examination'] = self.object.examination
        ctx['patient'] = self.object.patient
        ctx['is_edit'] = True
        # Mevcut ilaçlarla dolu formset
        ctx['item_formset'] = PrescriptionItemFormSet(
            self.request.POST or None,
            instance=self.object,
        )
        try:
            ctx['allergies'] = self.object.patient.medical_info.allergies
        except Exception:
            ctx['allergies'] = ''
        return ctx

    def form_valid(self, form):
        item_formset = PrescriptionItemFormSet(self.request.POST, instance=self.object)
        if not item_formset.is_valid():
            messages.error(self.request, f'İlaç bilgilerinde hata: {item_formset.errors}')
            return self.form_invalid(form)

        has_items = any(
            f.cleaned_data.get('medicine_name') and not f.cleaned_data.get('DELETE', False)
            for f in item_formset.forms
        )
        if not has_items:
            messages.error(self.request, 'En az bir ilaç eklemelisiniz.')
            return self.form_invalid(form)

        self.object = form.save()
        item_formset.instance = self.object
        item_formset.save()

        create_audit_log(
            self.request, 'UPDATE', 'Prescription', self.object.pk,
            f'Reçete güncellendi: {self.object.patient.full_name}'
        )
        messages.success(self.request, 'Reçete güncellendi.')
        return redirect(self.get_success_url())

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


class PrescriptionPrintView(LoginRequiredMixin, DetailView):
    """Tarayıcı baskısı için HTML reçete görünümü."""
    model = Prescription
    template_name = 'prescriptions/print.html'
    context_object_name = 'prescription'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['items'] = self.object.items.all()
        return ctx


class PrescriptionListView(LoginRequiredMixin, ListView):
    model = Prescription
    template_name = 'prescriptions/list.html'
    context_object_name = 'prescriptions'
    paginate_by = 30

    def get_queryset(self):
        qs = Prescription.objects.select_related(
            'patient', 'doctor__user', 'examination'
        ).order_by('-created_at')
        user = self.request.user
        if user.is_doctor:
            try:
                qs = qs.filter(doctor=user.doctor_profile)
            except Exception:
                pass

        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(patient__name__icontains=q) |
                Q(patient__surname__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        return ctx
