import os
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from patients.models import Patient
from examinations.models import Examination


ALLOWED_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.webp',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx',
}


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            f'Desteklenmeyen dosya türü: {ext}. İzin verilenler: {", ".join(ALLOWED_EXTENSIONS)}'
        )


def validate_file_size(value):
    limit = getattr(settings, 'FILE_UPLOAD_MAX_MEMORY_SIZE', 20971520)
    if value.size > limit:
        raise ValidationError(f'Dosya boyutu {limit // 1048576} MB sınırını aşıyor.')


def patient_document_path(instance, filename):
    safe_name = ''.join(c for c in filename if c.isalnum() or c in '._-')
    return f'patients/{instance.patient.pk}/documents/{safe_name}'


class DocumentCategory(models.TextChoices):
    LAB = 'LAB', 'Laboratuvar'
    RADIOLOGY = 'RADIOLOGY', 'Radyoloji'
    PHOTO = 'PHOTO', 'Fotoğraf'
    CONSENT = 'CONSENT', 'Onam Formu'
    PRESCRIPTION = 'PRESCRIPTION', 'Reçete'
    REPORT = 'REPORT', 'Rapor'
    ID_INSURANCE = 'ID_INSURANCE', 'Kimlik / Sigorta'
    OTHER = 'OTHER', 'Diğer'


class Document(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='documents', verbose_name='Hasta')
    examination = models.ForeignKey(
        Examination, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='documents', verbose_name='Muayene'
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        verbose_name='Yükleyen'
    )
    category = models.CharField(
        max_length=20, choices=DocumentCategory.choices,
        default=DocumentCategory.OTHER, verbose_name='Kategori'
    )
    file = models.FileField(
        upload_to=patient_document_path,
        validators=[validate_file_extension, validate_file_size],
        verbose_name='Dosya',
    )
    original_filename = models.CharField(max_length=255, verbose_name='Orijinal Dosya Adı')
    description = models.CharField(max_length=300, blank=True, verbose_name='Açıklama')
    file_size = models.PositiveIntegerField(default=0, verbose_name='Dosya Boyutu (bayt)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yükleme Tarihi')
    annotations = models.JSONField(default=dict, blank=True, verbose_name='Notlar')

    class Meta:
        verbose_name = 'Belge'
        verbose_name_plural = 'Belgeler'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.patient} - {self.original_filename}'

    def save(self, *args, **kwargs):
        if self.file and not self.original_filename:
            self.original_filename = self.file.name
        if self.file:
            try:
                self.file_size = self.file.size
            except Exception:
                pass
        super().save(*args, **kwargs)

    @property
    def is_image(self):
        ext = os.path.splitext(self.original_filename)[1].lower()
        return ext in {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
