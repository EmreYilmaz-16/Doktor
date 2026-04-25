import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect

from core.mixins import create_audit_log
from .models import Appointment, AppointmentStatus, Doctor
from .forms import AppointmentForm


class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/list.html'
    context_object_name = 'appointments'
    paginate_by = 30

    def get_queryset(self):
        qs = super().get_queryset().select_related('patient', 'doctor__user')
        doctor_id = self.request.GET.get('doctor')
        status = self.request.GET.get('status')
        date_str = self.request.GET.get('date')
        if doctor_id:
            qs = qs.filter(doctor_id=doctor_id)
        if status:
            qs = qs.filter(status=status)
        if date_str:
            qs = qs.filter(appointment_start__date=date_str)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['doctors'] = Doctor.objects.filter(status=True).select_related('user')
        ctx['statuses'] = AppointmentStatus.choices
        return ctx


class AppointmentCalendarView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/calendar.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['doctors'] = Doctor.objects.filter(status=True).select_related('user')
        return ctx


class AppointmentCalendarApiView(LoginRequiredMixin, View):
    def get(self, request):
        start = request.GET.get('start', '')
        end = request.GET.get('end', '')
        doctor_id = request.GET.get('doctor', '')
        qs = Appointment.objects.select_related('patient', 'doctor__user')
        if start:
            qs = qs.filter(appointment_start__gte=start)
        if end:
            qs = qs.filter(appointment_end__lte=end)
        if doctor_id:
            qs = qs.filter(doctor_id=doctor_id)

        status_colors = {
            'PENDING': '#6c757d',
            'CONFIRMED': '#0d6efd',
            'ARRIVED': '#0dcaf0',
            'IN_EXAM': '#fd7e14',
            'COMPLETED': '#198754',
            'CANCELLED': '#dc3545',
            'NO_SHOW': '#dc3545',
            'RESCHEDULED': '#ffc107',
        }
        events = []
        for apt in qs:
            events.append({
                'id': apt.pk,
                'title': f'{apt.patient.full_name}',
                'start': apt.appointment_start.isoformat(),
                'end': apt.appointment_end.isoformat(),
                'color': apt.doctor.color if apt.doctor.color else status_colors.get(apt.status, '#0d6efd'),
                'url': f'/randevular/{apt.pk}/',
                'extendedProps': {
                    'status': apt.get_status_display(),
                    'doctor': str(apt.doctor),
                    'type': apt.get_appointment_type_display(),
                }
            })
        return JsonResponse(events, safe=False)


class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'appointments/detail.html'
    context_object_name = 'appointment'


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/form.html'
    success_url = reverse_lazy('appointments:calendar')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        create_audit_log(
            self.request, 'CREATE', 'Appointment', self.object.pk,
            f'Randevu oluşturuldu: {self.object}'
        )
        messages.success(self.request, 'Randevu başarıyla oluşturuldu.')
        return response

    def get_initial(self):
        initial = super().get_initial()
        patient_id = self.request.GET.get('patient')
        if patient_id:
            initial['patient'] = patient_id
        return initial


class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/form.html'

    def get_success_url(self):
        return reverse_lazy('appointments:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        create_audit_log(
            self.request, 'UPDATE', 'Appointment', self.object.pk,
            f'Randevu güncellendi: {self.object}'
        )
        messages.success(self.request, 'Randevu güncellendi.')
        return response


class AppointmentStatusUpdateView(LoginRequiredMixin, View):
    """AJAX ile randevu durumu güncelleme."""
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        new_status = request.POST.get('status')
        if new_status not in [s[0] for s in AppointmentStatus.choices]:
            return JsonResponse({'error': 'Geçersiz durum'}, status=400)
        old_status = appointment.status
        appointment.status = new_status
        appointment.save(update_fields=['status', 'updated_at'])
        create_audit_log(
            request, 'STATUS_CHANGE', 'Appointment', pk,
            f'Randevu durumu: {old_status} → {new_status}'
        )
        return JsonResponse({'status': appointment.get_status_display()})
