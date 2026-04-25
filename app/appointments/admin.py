from django.contrib import admin
from .models import Doctor, Branch, Appointment


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'branch', 'status')
    list_filter = ('branch', 'status')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_start', 'status')
    list_filter = ('status', 'appointment_type', 'doctor')
    search_fields = ('patient__name', 'patient__surname')
