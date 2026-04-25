from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from datetime import date

from core.mixins import create_audit_log
from patients.models import Patient
from .models import Payment
from .forms import PaymentForm


class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'payments/list.html'
    context_object_name = 'payments'
    paginate_by = 30

    def get_queryset(self):
        qs = super().get_queryset().select_related('patient', 'service')
        date_str = self.request.GET.get('date')
        status = self.request.GET.get('status')
        if date_str:
            qs = qs.filter(created_at__date=date_str)
        if status:
            qs = qs.filter(payment_status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()
        ctx['today_total'] = (
            Payment.objects.filter(created_at__date=today, payment_status='PAID')
            .aggregate(total=Sum('amount'))['total'] or 0
        )
        return ctx


class PatientPaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payments/form.html'

    def dispatch(self, request, *args, **kwargs):
        self.patient = get_object_or_404(Patient, pk=kwargs['patient_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['patient'] = self.patient
        return kwargs

    def get_initial(self):
        return {'patient': self.patient}

    def form_valid(self, form):
        form.instance.patient = self.patient
        response = super().form_valid(form)
        create_audit_log(
            self.request, 'CREATE', 'Payment', self.object.pk,
            f'Ödeme kaydedildi: {self.patient.full_name} - {self.object.amount} TL'
        )
        messages.success(self.request, 'Ödeme kaydedildi.')
        return response

    def get_success_url(self):
        return reverse_lazy('patients:detail', kwargs={'pk': self.patient.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['patient'] = self.patient
        return ctx
