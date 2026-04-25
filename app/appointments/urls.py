from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.AppointmentListView.as_view(), name='list'),
    path('takvim/', views.AppointmentCalendarView.as_view(), name='calendar'),
    path('api/etkinlikler/', views.AppointmentCalendarApiView.as_view(), name='calendar_api'),
    path('yeni/', views.AppointmentCreateView.as_view(), name='create'),
    path('<int:pk>/', views.AppointmentDetailView.as_view(), name='detail'),
    path('<int:pk>/duzenle/', views.AppointmentUpdateView.as_view(), name='update'),
    path('<int:pk>/durum/', views.AppointmentStatusUpdateView.as_view(), name='status_update'),
]
