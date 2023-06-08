from django.core.management.base import BaseCommand
from app.models import UrlSegment, Page
import json
from google_tools import categorize_url

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-m', nargs='+', type=str)

    def handle(self, *args, **options):
        print(options)
        mdl = 'segment'
        segs = UrlSegment.objects.all()
        field = 'segment'
        if 'date_str' in options:
            mdl = options['date_str'][0]
        if mdl != 'segment':
            segs = Page.objects.all()
            field = 'url'
        for s in segs:
            d = categorize_url(s.segment)
            s.__dict__.update(d)
            s.save()






