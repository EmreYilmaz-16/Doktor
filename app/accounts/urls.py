from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('giris/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('cikis/', LogoutView.as_view(), name='logout'),
    path('kullanicilar/', views.UserListView.as_view(), name='user_list'),
    path('kullanicilar/yeni/', views.UserCreateView.as_view(), name='user_create'),
    path('kullanicilar/<int:pk>/duzenle/', views.UserUpdateView.as_view(), name='user_update'),
    path('sifre-degistir/', views.ChangePasswordView.as_view(), name='change_password'),
]
