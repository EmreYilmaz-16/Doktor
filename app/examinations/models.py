from django.db import models
from patients.models import Patient
from appointments.models import Doctor, Appointment


class Examination(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='examinations', verbose_name='Hasta')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='examinations', verbose_name='Doktor')
    appointment = models.OneToOneField(
        Appointment, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='examination', verbose_name='Randevu'
    )
    complaint = models.TextField(blank=True, verbose_name='Şikayet')
    anamnesis = models.TextField(blank=True, verbose_name='Anamnez / Hikaye')
    findings = models.TextField(blank=True, verbose_name='Fizik Muayene Bulguları')
    pre_diagnosis = models.CharField(max_length=300, blank=True, verbose_name='Ön Tanı')
    diagnosis = models.CharField(max_length=300, blank=True, verbose_name='Kesin Tanı')
    icd10_code = models.CharField(max_length=20, blank=True, verbose_name='ICD-10 Kodu')
    treatment_plan = models.TextField(blank=True, verbose_name='Tedavi Planı')
    doctor_note = models.TextField(blank=True, verbose_name='Doktor Notu (İç)')
    result = models.TextField(blank=True, verbose_name='Muayene Sonucu')
    control_date = models.DateField(null=True, blank=True, verbose_name='Kontrol Tarihi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Muayene Tarihi')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Muayene'
        verbose_name_plural = 'Muayeneler'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.patient} - {self.created_at:%d.%m.%Y}'


class VitalSigns(models.Model):
    examination = models.OneToOneField(
        Examination, on_delete=models.CASCADE, related_name='vitals', verbose_name='Muayene'
    )
    height = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name='Boy (cm)')
    weight = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name='Kilo (kg)')
    bmi = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='VKİ')
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name='Ateş (°C)')
    pulse = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Nabız (bpm)')
    systolic_bp = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Sistolik KB')
    diastolic_bp = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Diastolik KB')
    respiratory_rate = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Solunum Sayısı')
    oxygen_saturation = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='SpO2 (%)')
    blood_glucose = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name='Kan Şekeri')
    pain_score = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Ağrı Skoru (0-10)')

    class Meta:
        verbose_name = 'Vital Bulgular'
        verbose_name_plural = 'Vital Bulgular'

    def save(self, *args, **kwargs):
        if self.height and self.weight and self.height > 0:
            h_m = float(self.height) / 100
            self.bmi = round(float(self.weight) / (h_m ** 2), 2)
        super().save(*args, **kwargs)
