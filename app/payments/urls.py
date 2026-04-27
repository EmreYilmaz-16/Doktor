from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.PaymentListView.as_view(), name='list'),
    path('hasta/<int:patient_pk>/yeni/', views.PatientPaymentCreateView.as_view(), name='create'),
    path('<int:pk>/sil/', views.PaymentDeleteView.as_view(), name='delete'),
    # Muayene hizmet (borçlandırma)
    path('muayene/<int:examination_pk>/hizmet-ekle/', views.ExaminationServiceAddView.as_view(), name='examination_add'),
    path('muayene-hizmet/<int:pk>/sil/', views.ExaminationServiceDeleteView.as_view(), name='service_delete'),
    # Hizmet fiyat listesi
    path('hizmetler/', views.ServiceListView.as_view(), name='service_list'),
    path('hizmetler/yeni/', views.ServiceCreateView.as_view(), name='service_create'),
    path('hizmetler/<int:pk>/duzenle/', views.ServiceUpdateView.as_view(), name='service_update'),
]
