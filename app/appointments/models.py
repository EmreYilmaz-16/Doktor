from django.db import models
from django.conf import settings
from patients.models import Patient


class Branch(models.Model):
    name = models.CharField(max_length=100, verbose_name='Branş Adı')

    class Meta:
        verbose_name = 'Branş'
        verbose_name_plural = 'Branşlar'

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='doctor_profile', verbose_name='Kullanıcı'
    )
    title = models.CharField(max_length=50, blank=True, verbose_name='Unvan')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Branş')
    diploma_no = models.CharField(max_length=50, blank=True, verbose_name='Diploma No')
    color = models.CharField(max_length=7, default='#0d6efd', verbose_name='Takvim Rengi')
    status = models.BooleanField(default=True, verbose_name='Aktif')

    class Meta:
        verbose_name = 'Doktor'
        verbose_name_plural = 'Doktorlar'

    def __str__(self):
        name = self.user.get_full_name() or self.user.username
        return f'{self.title} {name}'.strip()


class AppointmentStatus(models.TextChoices):
    PENDING = 'PENDING', 'Bekliyor'
    CONFIRMED = 'CONFIRMED', 'Onaylandı'
    ARRIVED = 'ARRIVED', 'Geldi'
    IN_EXAM = 'IN_EXAM', 'Muayenede'
    COMPLETED = 'COMPLETED', 'Tamamlandı'
    CANCELLED = 'CANCELLED', 'İptal Edildi'
    NO_SHOW = 'NO_SHOW', 'Gelmedi'
    RESCHEDULED = 'RESCHEDULED', 'Ertelendi'


class AppointmentType(models.TextChoices):
    REGULAR = 'REGULAR', 'Normal Muayene'
    CONTROL = 'CONTROL', 'Kontrol'
    EMERGENCY = 'EMERGENCY', 'Acil'
    ONLINE = 'ONLINE', 'Online'


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments', verbose_name='Hasta')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments', verbose_name='Doktor')
    appointment_start = models.DateTimeField(verbose_name='Randevu Başlangıcı')
    appointment_end = models.DateTimeField(verbose_name='Randevu Bitişi')
    status = models.CharField(max_length=20, choices=AppointmentStatus.choices, default=AppointmentStatus.PENDING, verbose_name='Durum')
    appointment_type = models.CharField(max_length=20, choices=AppointmentType.choices, default=AppointmentType.REGULAR, verbose_name='Tür')
    note = models.TextField(blank=True, verbose_name='Not')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name='created_appointments', verbose_name='Oluşturan'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Randevu'
        verbose_name_plural = 'Randevular'
        ordering = ['-appointment_start']

    def __str__(self):
        return f'{self.patient} - {self.doctor} - {self.appointment_start:%d.%m.%Y %H:%M}'
