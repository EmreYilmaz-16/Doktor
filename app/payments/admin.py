from django.contrib import admin
from .models import Payment, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'status')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'amount', 'payment_type', 'description', 'created_at')
    list_filter = ('payment_type',)
    search_fields = ('patient__name', 'patient__surname')
