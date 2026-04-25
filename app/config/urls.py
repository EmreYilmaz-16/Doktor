from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('yonetim/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('hesap/', include('accounts.urls', namespace='accounts')),
    path('hastalar/', include('patients.urls', namespace='patients')),
    path('randevular/', include('appointments.urls', namespace='appointments')),
    path('muayeneler/', include('examinations.urls', namespace='examinations')),
    path('receteler/', include('prescriptions.urls', namespace='prescriptions')),
    path('belgeler/', include('documents.urls', namespace='documents')),
    path('odemeler/', include('payments.urls', namespace='payments')),
    path('raporlar/', include('reports.urls', namespace='reports')),
]

# Media dosyaları için - üretimde Nginx'e bırakılır; ancak Django üzerinden erişim denetimi için view'a yönlendiriyoruz
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
