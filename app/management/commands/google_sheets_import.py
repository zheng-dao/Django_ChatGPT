from django.core.management.base import BaseCommand
from app.models import AnalyticsPlatform, DataSummary, Sheet
import google_tools
from file_tools import merge_dicts
import json
from django.forms.models import model_to_dict

class Command(BaseCommand):
    help = 'nightly code to check google sheets and import data'

    def handle(self, *args, **options):
        sheets_name = Sheet.objects.filter(is_active=True)
        for n in sheets_name:
            try:
                print(n.name)
                google_tools.import_api_data('gs', None, n.name, is_sheet_name=True)
                print("Success")
            except Exception as e:
                if n.name:
                    print(n.name, e)
                else:
                    print(e)
                print("Error!")

