from django.urls import path
from . import views

app_name = 'examinations'

urlpatterns = [
    path('hasta/<int:patient_pk>/yeni/', views.ExaminationCreateView.as_view(), name='create'),
    path('hasta/<int:patient_pk>/randevu/<int:appointment_pk>/yeni/', views.ExaminationCreateView.as_view(), name='create_from_appointment'),
    path('<int:pk>/', views.ExaminationDetailView.as_view(), name='detail'),
    path('<int:pk>/duzenle/', views.ExaminationUpdateView.as_view(), name='update'),
]
