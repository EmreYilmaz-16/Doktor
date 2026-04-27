from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Sum
from datetime import date

from core.mixins import create_audit_log
from patients.models import Patient
from examinations.models import Examination, ExaminationService
from .models import Payment, Service
from .forms import PaymentForm


class PaymentListView(LoginRequiredMixin, ListView):
    """Kasa defteri — tahsil edilen tüm ödemeler."""
    model = Payment
    template_name = 'payments/list.html'
    context_object_name = 'payments'
    paginate_by = 50

    def get_queryset(self):
        qs = Payment.objects.select_related('patient').order_by('-created_at')
        date_str = self.request.GET.get('date')
        if date_str:
            qs = qs.filter(created_at__date=date_str)
        q = self.request.GET.get('q', '').strip()
        if q:
            from django.db.models import Q
            qs = qs.filter(
                Q(patient__name__icontains=q) | Q(patient__surname__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()
        ctx['today_total'] = (
            Payment.objects.filter(created_at__date=today)
            .aggregate(t=Sum('amount'))['t'] or 0
        )
        ctx['today_count'] = Payment.objects.filter(created_at__date=today).count()
        ctx['request'] = self.request
        return ctx


class PatientPaymentCreateView(LoginRequiredMixin, CreateView):
    """Hastaya doğrudan tahsilat ekle."""
    model = Payment
    form_class = PaymentForm
    template_name = 'payments/form.html'

    def dispatch(self, request, *args, **kwargs):
        self.patient = get_object_or_404(Patient, pk=kwargs['patient_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.patient = self.patient
        response = super().form_valid(form)
        create_audit_log(
            self.request, 'CREATE', 'Payment', self.object.pk,
            f'Tahsilat: {self.patient.full_name} - {self.object.amount} TL ({self.object.get_payment_type_display()})'
        )
        messages.success(self.request, f'{self.object.amount} ₺ tahsil edildi.')
        return response

    def get_success_url(self):
        return reverse_lazy('patients:detail', kwargs={'pk': self.patient.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['patient'] = self.patient
        return ctx


class PaymentDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        patient_pk = payment.patient_id
        create_audit_log(request, 'DELETE', 'Payment', pk, f'Tahsilat silindi: {payment.amount} TL')
        payment.delete()
        messages.success(request, 'Tahsilat silindi.')
        next_url = request.POST.get('next', '')
        if next_url:
            return redirect(next_url)
        return redirect('patients:detail', pk=patient_pk)


# ── Muayene Hizmet (Borçlandırma) ──────────────────────────────────────────

class ExaminationServiceAddView(LoginRequiredMixin, View):
    """Muayeneye hizmet/borçlandırma kalemi ekle."""

    def post(self, request, examination_pk):
        examination = get_object_or_404(Examination, pk=examination_pk)

        service_pk = request.POST.get('service')
        description = request.POST.get('description', '').strip()
        amount_str = request.POST.get('amount', '').strip()
        discount_str = request.POST.get('discount', '0').strip()

        service = None
        if service_pk:
            service = get_object_or_404(Service, pk=service_pk)

        try:
            amount = float(amount_str) if amount_str else (float(service.price) if service else None)
        except (ValueError, TypeError):
            amount = None

        if not amount:
            messages.error(request, 'Tutar girilmedi.')
            return redirect('examinations:detail', pk=examination_pk)

        try:
            discount = float(discount_str) if discount_str else 0
        except (ValueError, TypeError):
            discount = 0

        ExaminationService.objects.create(
            examination=examination,
            service=service,
            description=description or (service.name if service else 'Muayene Hizmeti'),
            amount=amount,
            discount=discount,
        )
        create_audit_log(
            request, 'CREATE', 'ExaminationService', None,
            f'Hizmet borçlandırıldı: {examination.patient.full_name} - {amount} TL'
        )
        messages.success(request, 'Hizmet eklendi.')
        return redirect('examinations:detail', pk=examination_pk)


class ExaminationServiceDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        svc = get_object_or_404(ExaminationService, pk=pk)
        examination_pk = svc.examination_id
        create_audit_log(request, 'DELETE', 'ExaminationService', pk, f'Hizmet silindi: {svc.amount} TL')
        svc.delete()
        messages.success(request, 'Hizmet silindi.')
        return redirect('examinations:detail', pk=examination_pk)


# ── Hizmet Fiyat Listesi ───────────────────────────────────────────────────

class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    template_name = 'payments/service_list.html'
    context_object_name = 'services'
    ordering = ['name']


class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    fields = ['name', 'price', 'status']
    template_name = 'payments/service_form.html'
    success_url = reverse_lazy('payments:service_list')

    def form_valid(self, form):
        messages.success(self.request, 'Hizmet eklendi.')
        return super().form_valid(form)


class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Service
    fields = ['name', 'price', 'status']
    template_name = 'payments/service_form.html'
    success_url = reverse_lazy('payments:service_list')

    def form_valid(self, form):
        messages.success(self.request, 'Hizmet güncellendi.')
        return super().form_valid(form)
