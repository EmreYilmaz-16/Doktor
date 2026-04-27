from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Sum, F, DecimalField, ExpressionWrapper, Value, OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from core.mixins import create_audit_log
from .models import Patient, PatientMedicalInfo, PatientConsent
from .forms import PatientForm, PatientMedicalInfoForm


def _balance_annotations(qs):
    """
    Hasta queryset'ine borç/alacak annotation'ları ekler.
    borç  = muayenelerdeki ExaminationService net toplamı (amount - discount)
    alacak = Payment toplamı
    Subquery kullanılır — çoklu JOIN'lerde row çarpılmasını önlemek için.
    """
    from examinations.models import ExaminationService
    from payments.models import Payment

    charges_subq = (
        ExaminationService.objects
        .filter(examination__patient=OuterRef('pk'))
        .values('examination__patient')
        .annotate(t=Sum(F('amount') - F('discount')))
        .values('t')
    )
    payments_subq = (
        Payment.objects
        .filter(patient=OuterRef('pk'))
        .values('patient')
        .annotate(t=Sum('amount'))
        .values('t')
    )
    return qs.annotate(
        total_charges=Coalesce(
            Subquery(charges_subq, output_field=DecimalField()),
            Value(0, output_field=DecimalField())
        ),
        total_payments=Coalesce(
            Subquery(payments_subq, output_field=DecimalField()),
            Value(0, output_field=DecimalField())
        ),
    )


class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'patients/list.html'
    context_object_name = 'patients'
    paginate_by = 25

    def get_queryset(self):
        qs = _balance_annotations(super().get_queryset()).order_by('surname', 'name')
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
        for patient in ctx['patients']:
            nb = patient.total_payments - patient.total_charges
            patient.net_balance = nb
            patient.display_balance = abs(nb)
            if nb < 0:
                patient.balance_type = 'debt'   # borçlu
            elif nb > 0:
                patient.balance_type = 'credit'  # alacaklı
            else:
                patient.balance_type = 'zero'
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
        ctx['payments'] = patient.payments.order_by('-created_at')[:30]

        # Borç / Alacak özeti (cari hesap)
        from examinations.models import ExaminationService
        svc_net = ExpressionWrapper(
            F('services__amount') - F('services__discount'),
            output_field=DecimalField()
        )
        exam_agg = patient.examinations.aggregate(
            total_charges=Coalesce(
                Sum(svc_net),
                Value(0, output_field=DecimalField())
            )
        )
        pay_agg = patient.payments.aggregate(
            total_payments=Coalesce(Sum('amount'), Value(0, output_field=DecimalField()))
        )
        total_charges = exam_agg['total_charges']
        total_payments = pay_agg['total_payments']
        ctx['total_charges'] = total_charges
        ctx['total_payments'] = total_payments
        # net: pozitif = alacak (fazla ödeme), negatif = borçlu
        ctx['net_balance'] = total_payments - total_charges

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


def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


class PatientConsentView(LoginRequiredMixin, View):
    """Hasta onay formlarını listele ve yeni onam kaydet."""

    def get(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        consents = patient.consents.all()
        consent_types = PatientConsent.ConsentType.choices
        return render(request, 'patients/consents.html', {
            'patient': patient,
            'consents': consents,
            'consent_types': consent_types,
        })

    def post(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        consent_type = request.POST.get('consent_type')
        approved = request.POST.get('approved') == 'true'
        notes = request.POST.get('notes', '')
        PatientConsent.objects.create(
            patient=patient,
            consent_type=consent_type,
            approved=approved,
            approved_at=timezone.now() if approved else None,
            approved_by=request.user,
            ip_address=_get_client_ip(request),
            notes=notes,
        )
        if approved:
            messages.success(request, 'Onam başarıyla kaydedildi.')
        else:
            messages.warning(request, 'Red/iptal onamı kaydedildi.')
        return redirect('patients:consents', pk=pk)
