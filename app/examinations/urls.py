from django.urls import path
from . import views

app_name = 'examinations'

urlpatterns = [
    path('', views.ExaminationListView.as_view(), name='list'),
    path('hasta/<int:patient_pk>/yeni/', views.ExaminationCreateView.as_view(), name='create'),
    path('hasta/<int:patient_pk>/randevu/<int:appointment_pk>/yeni/', views.ExaminationCreateView.as_view(), name='create_from_appointment'),
    path('<int:pk>/', views.ExaminationDetailView.as_view(), name='detail'),
    path('<int:pk>/duzenle/', views.ExaminationUpdateView.as_view(), name='update'),
    # Şablonlar
    path('sablonlar/', views.ExaminationTemplateListView.as_view(), name='template_list'),
    path('sablonlar/yeni/', views.ExaminationTemplateCreateView.as_view(), name='template_create'),
    path('sablonlar/<int:pk>/duzenle/', views.ExaminationTemplateUpdateView.as_view(), name='template_update'),
    path('sablonlar/<int:pk>/sil/', views.ExaminationTemplateDeleteView.as_view(), name='template_delete'),
    path('sablonlar/<int:pk>/api/', views.ExaminationTemplateApiView.as_view(), name='template_api'),
    # ICD-10 autocomplete
    path('icd10/ara/', views.ICD10SearchView.as_view(), name='icd10_search'),
]
