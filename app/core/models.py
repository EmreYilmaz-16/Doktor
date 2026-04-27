from django.db import models
from django.conf import settings


class AuditLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Kullanıcı',
    )
    action = models.CharField(max_length=50, verbose_name='İşlem')
    entity_type = models.CharField(max_length=50, verbose_name='Kayıt Türü')
    entity_id = models.BigIntegerField(null=True, blank=True, verbose_name='Kayıt ID')
    description = models.TextField(blank=True, verbose_name='Açıklama')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP Adresi')
    user_agent = models.CharField(max_length=255, blank=True, verbose_name='Tarayıcı')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Tarih')

    class Meta:
        verbose_name = 'İşlem Kaydı'
        verbose_name_plural = 'İşlem Kayıtları'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.created_at:%d.%m.%Y %H:%M} - {self.user} - {self.action}'


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        INFO = 'INFO', 'Bilgi'
        WARNING = 'WARNING', 'Uyarı'
        SUCCESS = 'SUCCESS', 'Başarı'
        APPOINTMENT = 'APPOINTMENT', 'Randevu'
        CONTROL = 'CONTROL', 'Kontrol'
        PAYMENT = 'PAYMENT', 'Ödeme'

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Alıcı',
    )
    notification_type = models.CharField(
        max_length=20, choices=NotificationType.choices,
        default=NotificationType.INFO, verbose_name='Tür',
    )
    title = models.CharField(max_length=200, verbose_name='Başlık')
    message = models.TextField(blank=True, verbose_name='Mesaj')
    link = models.CharField(max_length=500, blank=True, verbose_name='Bağlantı')
    is_read = models.BooleanField(default=False, verbose_name='Okundu')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Tarih')

    class Meta:
        verbose_name = 'Bildirim'
        verbose_name_plural = 'Bildirimler'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.recipient} — {self.title}'
