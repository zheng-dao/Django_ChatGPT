from django.contrib import messages
from django.shortcuts import render, redirect
from functools import wraps
from .models import *
from django.urls import reverse

def check_perms(user, allow_fi=False):
    allow = False
    if user.is_superuser or user.is_staff:
        allow = True
    elif allow_fi and user.company.is_subscriber and user.company.is_active:
        allow = True
    return allow

def check_perms_fi(user, allow_fi=True):
    return check_perms(user, allow_fi)

def check_mfa_setup(view_func):
    def _decorator(request, *args, **kwargs):
        from app.views import is_mfa_setup_invalid
        user = request.user
        if is_mfa_setup_invalid(user):
            return redirect('two_factor:setup')
        response = view_func(request, *args, **kwargs)
        return response
    return wraps(view_func)(_decorator)        

def check_cu_user(view_func):
    def _decorator(request, *args, **kwargs):
        company_code = None
        for key,value in kwargs.items():
            company_code = value if key=='company_code' else None
        
        is_dir_enabled = request.path.endswith('dir/') or request.path.endswith('dir')
        print('is_dir_enabled', is_dir_enabled)

        current_user_groups = request.user.groups.values_list('name', flat=True)
        if (current_user_groups and not request.user.is_superuser and request.user.is_staff) and ('personalization_admin' in current_user_groups or 'personalization_staff' in current_user_groups):
            if (company_code != request.user.userprofile.company.code and is_dir_enabled) or (company_code == request.user.userprofile.company.code and is_dir_enabled) or (company_code != request.user.userprofile.company.code and not is_dir_enabled):
                
                user_company_code = request.user.userprofile.company.code
                default_image_width = list(Asset.objects.values_list('width').filter(company__code=user_company_code).distinct().order_by('-width').annotate(count_images=Count('width')).first())[0]
                return redirect('/images/'+str(user_company_code)+"?image_width="+str(default_image_width))

        response = view_func(request, *args, **kwargs)
        return response
    return wraps(view_func)(_decorator)

def check_cu_user_revised(view_func):
    def _decorator(request, *args, **kwargs):
        company_code = None
        for key,value in kwargs.items():
            company_code = value if key=='company_code' else None
        
        is_dir_enabled = request.path.endswith('dir/') or request.path.endswith('dir')
        print('is_dir_enabled', is_dir_enabled)

        current_user_groups = request.user.groups.values_list('name', flat=True)
        if (current_user_groups and not request.user.is_superuser and request.user.is_staff) and ('personalization_admin' in current_user_groups or 'personalization_staff' in current_user_groups):
            if (company_code != request.user.userprofile.company.code and is_dir_enabled) or (company_code == request.user.userprofile.company.code and is_dir_enabled) or (company_code != request.user.userprofile.company.code and not is_dir_enabled):
                
                user_company_code = request.user.userprofile.company.code
                default_image_width = list(Asset.objects.values_list('width').filter(company__code=user_company_code).distinct().order_by('-width').annotate(count_images=Count('width')).first())[0]
                user_company_code = str(user_company_code)
                return redirect(reverse('z-media-library-company-code', kwargs={'company_code': user_company_code} )+"?image_width="+str(default_image_width))

        response = view_func(request, *args, **kwargs)
        return response
    return wraps(view_func)(_decorator)    