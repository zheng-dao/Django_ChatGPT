from django.core.management.base import BaseCommand
from pmodels import ptest, get_test_data
from django.conf import settings
from datetime import date
from django.core.mail import send_mail

class Command(BaseCommand):
    #def add_arguments(self, parser):
    #    parser.add_argument('-co', nargs='+', type=str)
    #    parser.add_argument('-w', type=int)

    def handle(self, *args, **options):
        print(options)
        if settings.ENV in ['stg', 'prod']:
            if settings.DEBUG:
                email_body = 'DEBUG setting is set to True on ' + settings.ENV
                subject = 'Debug is set to True on ' + settings.ENV + ': ' + str(date.today())
                send_mail(subject, email_body, settings.DEFAULT_FROM_EMAIL, settings.NOTIFICATIONS['admins'])
