from django.db import models
from patients.models import Patient
from appointments.models import Appointment, Doctor
from examinations.models import Examination


class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name='Hizmet Adı')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Fiyat')
    status = models.BooleanField(default=True, verbose_name='Aktif')

    class Meta:
        verbose_name = 'Hizmet'
        verbose_name_plural = 'Hizmetler'

    def __str__(self):
        return f'{self.name} - {self.price} TL'


class Payment(models.Model):
    class PaymentType(models.TextChoices):
        CASH = 'CASH', 'Nakit'
        CARD = 'CARD', 'Kredi / Banka Kartı'
        TRANSFER = 'TRANSFER', 'Havale / EFT'
        INSURANCE = 'INSURANCE', 'Sigorta'
        OTHER = 'OTHER', 'Diğer'

    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Bekliyor'
        PAID = 'PAID', 'Ödendi'
        PARTIAL = 'PARTIAL', 'Kısmi Ödeme'
        REFUNDED = 'REFUNDED', 'İade Edildi'
        CANCELLED = 'CANCELLED', 'İptal'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='payments', verbose_name='Hasta')
    appointment = models.ForeignKey(
        Appointment, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='payments', verbose_name='Randevu'
    )
    examination = models.ForeignKey(
        Examination, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='payments', verbose_name='Muayene'
    )
    service = models.ForeignKey(
        Service, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Hizmet'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Tutar')
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='İndirim')
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices, default=PaymentType.CASH, verbose_name='Ödeme Türü')
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING, verbose_name='Ödeme Durumu')
    description = models.CharField(max_length=300, blank=True, verbose_name='Açıklama')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Tarih')

    class Meta:
        verbose_name = 'Ödeme'
        verbose_name_plural = 'Ödemeler'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.patient} - {self.amount} TL - {self.get_payment_status_display()}'

    @property
    def net_amount(self):
        return self.amount - self.discount
