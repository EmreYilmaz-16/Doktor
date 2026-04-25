from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    ADMIN = 'ADMIN', 'Sistem Yöneticisi'
    DOCTOR = 'DOCTOR', 'Doktor'
    SECRETARY = 'SECRETARY', 'Sekreter'
    ACCOUNTANT = 'ACCOUNTANT', 'Muhasebe'
    PATIENT = 'PATIENT', 'Hasta'


class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.SECRETARY,
        verbose_name='Rol',
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name='Telefon')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')

    class Meta:
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.get_role_display()})'

    @property
    def is_admin(self):
        return self.role == Role.ADMIN

    @property
    def is_doctor(self):
        return self.role == Role.DOCTOR

    @property
    def is_secretary(self):
        return self.role == Role.SECRETARY

    @property
    def is_accountant(self):
        return self.role == Role.ACCOUNTANT
