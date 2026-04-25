from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.PaymentListView.as_view(), name='list'),
    path('hasta/<int:patient_pk>/yeni/', views.PatientPaymentCreateView.as_view(), name='create'),
]
