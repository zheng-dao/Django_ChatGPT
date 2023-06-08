from django.core.management.base import BaseCommand
from secure_tools import check_user_inactivity, expire_passwords

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        users_inactive = check_user_inactivity(days_inactive=90)
        if users_inactive:
            for user in users_inactive:
                user.is_active = False
                user.save()

        expire_passwords(days_active=90)

