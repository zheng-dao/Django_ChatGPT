from django.conf import settings
from rest_framework.permissions import BasePermission #DjangoModelPermissionsOrAnonReadOnly, AllowAny, IsAuthenticated, DjangoModelPermissions, 

class SafelistPermission(BasePermission):
    """
    Ensure the request's IP address is on the safe list configured in Django settings.
    """
    def has_permission(self, request, view):
        print('checking IP for permissions')
        remote_addr = remote_host = ''
        if 'REMOTE_ADDR' in request.META:
            remote_addr = request.META['REMOTE_ADDR']
        if 'REMOTE_HOST' in request.META:
            remote_host = request.META['REMOTE_HOST']
        if remote_host in settings.REST_SAFE_LIST_IPS:
            return True
        for valid_ip in settings.REST_SAFE_LIST_IPS:
            if remote_addr == valid_ip or remote_addr.startswith(valid_ip):
                return True
        return False

