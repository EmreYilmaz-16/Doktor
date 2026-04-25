from django.contrib import admin
from .models import Examination, VitalSigns


class VitalSignsInline(admin.StackedInline):
    model = VitalSigns
    extra = 0


@admin.register(Examination)
class ExaminationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'created_at', 'diagnosis')
    list_filter = ('doctor',)
    search_fields = ('patient__name', 'patient__surname', 'diagnosis')
    inlines = [VitalSignsInline]
