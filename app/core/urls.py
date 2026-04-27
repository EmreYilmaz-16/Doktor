from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('islem-kayitlari/', views.AuditLogListView.as_view(), name='audit_logs'),
    path('bildirimler/', views.NotificationListView.as_view(), name='notifications'),
    path('bildirimler/okundu/', views.NotificationMarkReadView.as_view(), name='notifications_mark_read'),
    path('bildirimler/<int:pk>/okundu/', views.NotificationMarkReadView.as_view(), name='notification_mark_read'),
    path('bildirimler/sayac/', views.NotificationUnreadCountView.as_view(), name='notification_count'),
    path('sekreter/', views.SecretaryDashboardView.as_view(), name='secretary_dashboard'),
]
