from django.core.management.base import BaseCommand, CommandError
from file_tools import save_csv, load_csv_data
from ncua_tools import calculate_benchmark, calculate_growth_rates, get_filename, get_mapping, series_full_form, \
    get_previous_years_data, calculate_growth, import_data
from app.models import AnalyticsPlatform, Company, DataSummary
from datetime import date
from timedate import get_qtr
from django.db import connections
from app.models import DataSummary, AnalyticsPlatform
import os
import shutil


class Command(BaseCommand):
    help = 'Delete records from data summary table for a given date'
    '''
    You can also input multiple dates.
    '''

    def add_arguments(self, parser):
        parser.add_argument('code_date', nargs='+', type=str)

    def handle(self, *args, **options):
        kwargs = {}; r=None
        code_date = options['code_date']
        code = code_date[0]
        yr = 'all'
        years = range(2014, date.today().year + 1)
        if len(code_date) == 2:
            yr = code_date[1]
            years = [yr]
            r = 'y'
        else:
            r = input('Are you sure you want to delete all years (y/n)?')
        if r.lower() == 'y':
            ap = AnalyticsPlatform.objects.get(code=code)
            for yr in years:
                kwargs['year'] = yr
                kwargs['analyticsplatform'] = ap
                #print(kwargs)
                obj = DataSummary.objects.filter(**kwargs).delete()
                print("%d records of year %s deleted successfully." % (obj[0], yr))
