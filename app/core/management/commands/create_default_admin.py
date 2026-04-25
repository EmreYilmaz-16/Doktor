from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Varsayılan admin kullanıcısını oluşturur (yoksa)'

    def handle(self, *args, **kwargs):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        username = settings.ADMIN_USERNAME
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=settings.ADMIN_EMAIL,
                password=settings.ADMIN_PASSWORD,
                role='ADMIN',
            )
            self.stdout.write(self.style.SUCCESS(f'Admin kullanıcısı oluşturuldu: {username}'))
        else:
            self.stdout.write(f'Admin kullanıcısı zaten mevcut: {username}')
