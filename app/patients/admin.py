from django.contrib import admin
from .models import Patient, PatientMedicalInfo, PatientConsent


class PatientMedicalInfoInline(admin.StackedInline):
    model = PatientMedicalInfo
    extra = 0


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'identity_no', 'phone', 'blood_type', 'status', 'created_at')
    search_fields = ('name', 'surname', 'identity_no', 'phone')
    list_filter = ('status', 'gender', 'blood_type')
    inlines = [PatientMedicalInfoInline]
