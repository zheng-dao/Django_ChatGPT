import os
from django.conf import settings
from app.models import UserProfile

def get_up(user):
    return UserProfile.objects.filter(user=user).first()

def is_fin_staff(user):
    is_staff = False
    suffix = user.email.split('@')[-1]
    if suffix in settings.STAFF_DOMAINS:
        is_staff = True
    return is_staff

def is_fi_staff(user):
    is_staff = False
    up = get_up(user)
    suffix = user.email.split('@')[-1]
    if up:
        domains = Domain.objects.filter(company=up.company)
        for domain in domains:
            if suffix == domain.name:
                is_staff = True
    return is_staff

def check_all_staff(user):
    is_staff = is_fin_staff(user)
    if not is_staff:
        is_staff = is_fi_staff(user)
    return is_staff
