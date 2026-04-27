from django.db import models
from django.conf import settings
from patients.models import Patient
from examinations.models import Examination
from appointments.models import Doctor


class Prescription(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Aktif'
        COMPLETED = 'COMPLETED', 'Tamamlandı'
        CANCELLED = 'CANCELLED', 'İptal'

    examination = models.ForeignKey(
        Examination, on_delete=models.CASCADE, related_name='prescriptions', verbose_name='Muayene'
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions', verbose_name='Hasta')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='prescriptions', verbose_name='Doktor')
    prescription_date = models.DateField(auto_now_add=True, verbose_name='Reçete Tarihi')
    note = models.TextField(blank=True, verbose_name='Reçete Notu')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE, verbose_name='Durum')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Reçete'
        verbose_name_plural = 'Reçeteler'
        ordering = ['-created_at']

    def __str__(self):
        return f'Reçete #{self.pk} - {self.patient} - {self.prescription_date}'


class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(
        Prescription, on_delete=models.CASCADE, related_name='items', verbose_name='Reçete'
    )
    medicine_name = models.CharField(max_length=200, verbose_name='İlaç Adı')
    active_ingredient = models.CharField(max_length=200, blank=True, verbose_name='Etken Madde')
    dosage = models.CharField(max_length=100, blank=True, verbose_name='Doz')
    frequency = models.CharField(max_length=100, blank=True, verbose_name='Kullanım Sıklığı')
    duration = models.CharField(max_length=100, blank=True, verbose_name='Kullanım Süresi')
    usage_instruction = models.TextField(blank=True, verbose_name='Kullanım Talimatı')
    note = models.CharField(max_length=300, blank=True, verbose_name='Not')

    class Meta:
        verbose_name = 'Reçete Kalemi'
        verbose_name_plural = 'Reçete Kalemleri'

    def __str__(self):
        return f'{self.medicine_name} - {self.dosage}'
