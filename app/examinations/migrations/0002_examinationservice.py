# Adım 1: ExaminationService tablosunu oluştur (payments migration'ından bağımsız)
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('examinations', '0001_initial'),
        ('payments', '0001_initial'),  # Service FK için
    ]

    operations = [
        migrations.CreateModel(
            name='ExaminationService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=300, verbose_name='Açıklama')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Tutar')),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='İndirim')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Tarih')),
                ('examination', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='services',
                    to='examinations.examination',
                    verbose_name='Muayene',
                )),
                ('service', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to='payments.service',
                    verbose_name='Hizmet',
                )),
            ],
            options={
                'verbose_name': 'Muayene Hizmeti',
                'verbose_name_plural': 'Muayene Hizmetleri',
                'ordering': ['created_at'],
            },
        ),
    ]
