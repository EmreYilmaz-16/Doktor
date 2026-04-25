from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect

from .models import AuditLog


class RoleRequiredMixin(AccessMixin):
    """İzin verilen roller listesini allowed_roles olarak tanımla."""
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.role not in self.allowed_roles and not request.user.is_admin:
            messages.error(request, 'Bu sayfaya erişim yetkiniz bulunmamaktadır.')
            return redirect('core:dashboard')
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['ADMIN']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_admin:
            messages.error(request, 'Bu sayfaya erişim yetkiniz bulunmamaktadır.')
            return redirect('core:dashboard')
        return super(RoleRequiredMixin, self).dispatch(request, *args, **kwargs)


class DoctorRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['DOCTOR']


class AuditMixin:
    """View'lerde otomatik işlem kaydı oluşturmak için mixin."""
    audit_action = ''
    audit_entity_type = ''

    def log_action(self, request, entity_id=None, description=''):
        if not self.audit_action:
            return
        AuditLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action=self.audit_action,
            entity_type=self.audit_entity_type or self.__class__.__name__,
            entity_id=entity_id,
            description=description,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:255],
        )


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def create_audit_log(request, action, entity_type, entity_id=None, description=''):
    AuditLog.objects.create(
        user=request.user if request.user.is_authenticated else None,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        description=description,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:255],
    )
