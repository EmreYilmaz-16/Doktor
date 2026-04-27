# Adım 3: Payment modelinden eski alanları kaldır
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_data_migration'),
    ]

    operations = [
        migrations.RemoveField(model_name='payment', name='appointment'),
        migrations.RemoveField(model_name='payment', name='discount'),
        migrations.RemoveField(model_name='payment', name='examination'),
        migrations.RemoveField(model_name='payment', name='payment_status'),
        migrations.RemoveField(model_name='payment', name='service'),
    ]
