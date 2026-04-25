from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('islem-kayitlari/', views.AuditLogListView.as_view(), name='audit_logs'),
]
