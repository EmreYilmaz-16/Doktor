from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.db.models import Sum
from datetime import date

from appointments.models import Appointment, AppointmentStatus
from patients.models import Patient
from payments.models import Payment
from .models import AuditLog


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()
        user = self.request.user

        appointments_qs = Appointment.objects.filter(appointment_start__date=today)
        if user.is_doctor:
            try:
                appointments_qs = appointments_qs.filter(doctor__user=user)
            except Exception:
                pass

        ctx['today_appointments'] = (
            appointments_qs
            .select_related('patient', 'doctor__user')
            .order_by('appointment_start')
        )
        ctx['waiting_count'] = appointments_qs.filter(status=AppointmentStatus.ARRIVED).count()
        ctx['today_count'] = appointments_qs.count()
        ctx['total_patients'] = Patient.objects.filter(status='ACTIVE').count()
        ctx['today_income'] = (
            Payment.objects.filter(created_at__date=today, payment_status='PAID')
            .aggregate(total=Sum('amount'))['total'] or 0
        )
        ctx['recent_logs'] = AuditLog.objects.select_related('user').order_by('-created_at')[:10]
        ctx['today'] = today
        return ctx


class AuditLogListView(LoginRequiredMixin, ListView):
    model = AuditLog
    template_name = 'core/audit_logs.html'
    context_object_name = 'logs'
    paginate_by = 50
    ordering = ['-created_at']
