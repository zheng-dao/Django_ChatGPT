from django.core.management.base import BaseCommand
from pmodels import ptest, get_test_data
from app.models import Company

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-co', nargs='+', type=str)

    def handle(self, *args, **options):
        print("arguments are =", options)
        print("command executed successfully")
        print('this is another line')
