from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('hasta/<int:patient_pk>/', views.DocumentListView.as_view(), name='list'),
    path('hasta/<int:patient_pk>/yukle/', views.DocumentUploadView.as_view(), name='upload'),
    path('<int:pk>/indir/', views.DocumentDownloadView.as_view(), name='download'),
    path('<int:pk>/sil/', views.DocumentDeleteView.as_view(), name='delete'),
    path('<int:pk>/notlar/', views.DocumentAnnotateView.as_view(), name='annotate'),
]
