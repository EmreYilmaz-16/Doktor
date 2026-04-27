from django.urls import path
from . import views

app_name = 'prescriptions'

urlpatterns = [
    path('', views.PrescriptionListView.as_view(), name='list'),
    path('muayene/<int:examination_pk>/yeni/', views.PrescriptionCreateView.as_view(), name='create'),
    path('<int:pk>/', views.PrescriptionDetailView.as_view(), name='detail'),
    path('<int:pk>/duzenle/', views.PrescriptionUpdateView.as_view(), name='update'),
    path('<int:pk>/pdf/', views.PrescriptionPdfView.as_view(), name='pdf'),
    path('<int:pk>/yazdir/', views.PrescriptionPrintView.as_view(), name='print'),
]
