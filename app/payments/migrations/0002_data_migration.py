# Adım 2: Mevcut muayene-bağlı Payment'ları ExaminationService'e taşı
from django.db import migrations


def migrate_exam_payments_to_services(apps, schema_editor):
    """Muayeneye bağlı Payment kayıtlarını ExaminationService'e kopyala."""
    Payment = apps.get_model('payments', 'Payment')
    ExaminationService = apps.get_model('examinations', 'ExaminationService')

    for pmt in Payment.objects.filter(examination__isnull=False):
        ExaminationService.objects.create(
            examination=pmt.examination,
            service=pmt.service,
            description=pmt.description or (pmt.service.name if pmt.service else 'Muayene Hizmeti'),
            amount=pmt.amount,
            discount=pmt.discount,
            # created_at auto_now_add, can't set it directly
        )

    # Standalone PENDING payments'ları sil (yeni modelde anlamlı değil)
    Payment.objects.filter(
        examination__isnull=True,
        payment_status__in=['PENDING', 'PARTIAL'],
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
        ('examinations', '0002_examinationservice'),
    ]

    operations = [
        migrations.RunPython(
            migrate_exam_payments_to_services,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
