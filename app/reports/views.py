from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate, TruncMonth
from datetime import date, timedelta
import json

from appointments.models import Appointment, AppointmentStatus
from patients.models import Patient
from payments.models import Payment
from examinations.models import Examination


class ReportDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()
        month_start = today.replace(day=1)

        # Son 30 günün günlük hasta sayısı
        last_30 = today - timedelta(days=29)
        daily_data = (
            Appointment.objects
            .filter(appointment_start__date__gte=last_30, status=AppointmentStatus.COMPLETED)
            .annotate(day=TruncDate('appointment_start'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        labels = [(last_30 + timedelta(days=i)).strftime('%d.%m') for i in range(30)]
        daily_map = {str(d['day']): d['count'] for d in daily_data}
        values = [daily_map.get(str(last_30 + timedelta(days=i)), 0) for i in range(30)]

        ctx['daily_labels'] = json.dumps(labels)
        ctx['daily_values'] = json.dumps(values)

        # Aylık gelir (son 6 ay)
        monthly_income = (
            Payment.objects
            .filter(payment_status='PAID')
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(total=Sum('amount'))
            .order_by('-month')[:6]
        )
        income_labels = [str(m['month'].strftime('%b %Y')) if m['month'] else '' for m in monthly_income]
        income_values = [float(m['total']) for m in monthly_income]
        ctx['income_labels'] = json.dumps(income_labels[::-1])
        ctx['income_values'] = json.dumps(income_values[::-1])

        # Genel istatistikler
        ctx['total_patients'] = Patient.objects.filter(status='ACTIVE').count()
        ctx['month_appointments'] = Appointment.objects.filter(
            appointment_start__date__gte=month_start
        ).count()
        ctx['month_income'] = (
            Payment.objects.filter(created_at__date__gte=month_start, payment_status='PAID')
            .aggregate(total=Sum('amount'))['total'] or 0
        )
        ctx['no_show_count'] = Appointment.objects.filter(
            appointment_start__date__gte=month_start, status=AppointmentStatus.NO_SHOW
        ).count()

        return ctx
