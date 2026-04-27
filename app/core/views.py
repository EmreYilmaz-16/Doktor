from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import JsonResponse
from django.db.models import Sum
from datetime import date, timedelta

from appointments.models import Appointment, AppointmentStatus
from patients.models import Patient
from payments.models import Payment
from .models import AuditLog, Notification


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
            Payment.objects.filter(created_at__date=today)
            .aggregate(total=Sum('amount'))['total'] or 0
        )
        ctx['recent_logs'] = AuditLog.objects.select_related('user').order_by('-created_at')[:10]
        ctx['today'] = today

        # Bekleyen (ARRIVED) hastalar — doktora hızlı muayene başlatma
        ctx['arrived_patients'] = (
            appointments_qs
            .filter(status=AppointmentStatus.ARRIVED)
            .select_related('patient', 'doctor__user')
            .order_by('appointment_start')
        )

        # Doktor paneli ekstra
        if user.is_doctor:
            try:
                from examinations.models import Examination
                doctor = user.doctor_profile
                ctx['today_examinations'] = Examination.objects.filter(
                    doctor=doctor, created_at__date=today
                ).count()
                ctx['upcoming_controls'] = (
                    Examination.objects.filter(
                        doctor=doctor,
                        control_date__lte=today + timedelta(days=7),
                        control_date__gte=today,
                    )
                    .select_related('patient')
                    .order_by('control_date')[:10]
                )
            except Exception:
                ctx['today_examinations'] = 0
                ctx['upcoming_controls'] = []

        return ctx


class AuditLogListView(LoginRequiredMixin, ListView):
    model = AuditLog
    template_name = 'core/audit_logs.html'
    context_object_name = 'logs'
    paginate_by = 50
    ordering = ['-created_at']


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'core/notifications.html'
    context_object_name = 'notifications'
    paginate_by = 30

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')

    def get(self, request, *args, **kwargs):
        # Listeyi açınca tüm bildirimleri okundu yap
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return super().get(request, *args, **kwargs)


class NotificationMarkReadView(LoginRequiredMixin, View):
    """AJAX: Tek bildirimi okundu işaretle veya tümünü temizle."""
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            Notification.objects.filter(pk=pk, recipient=request.user).update(is_read=True)
        else:
            Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        unread = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return JsonResponse({'unread': unread})


class NotificationUnreadCountView(LoginRequiredMixin, View):
    """AJAX: Okunmamış bildirim sayısını döndür."""
    def get(self, request, *args, **kwargs):
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return JsonResponse({'count': count})


class SecretaryDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/secretary_dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()

        all_today = (
            Appointment.objects.filter(appointment_start__date=today)
            .select_related('patient', 'doctor__user')
            .order_by('appointment_start')
        )
        ctx['today_appointments'] = all_today
        ctx['today_count'] = all_today.count()
        ctx['waiting_count'] = all_today.filter(status=AppointmentStatus.ARRIVED).count()
        ctx['scheduled_count'] = all_today.filter(status__in=[AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED]).count()
        ctx['done_count'] = all_today.filter(status=AppointmentStatus.COMPLETED).count()
        ctx['arrived_patients'] = all_today.filter(status=AppointmentStatus.ARRIVED)
        ctx['total_patients'] = Patient.objects.filter(status='ACTIVE').count()
        ctx['today_income'] = (
            Payment.objects.filter(created_at__date=today)
            .aggregate(total=Sum('amount'))['total'] or 0
        )
        ctx['recent_patients'] = Patient.objects.order_by('-created_at')[:5]
        ctx['today'] = today
        return ctx
