from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='annotations',
            field=models.JSONField(blank=True, default=dict, verbose_name='Notlar'),
        ),
    ]
