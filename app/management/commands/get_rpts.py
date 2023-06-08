from django.core.management.base import BaseCommand
from pmodels import ptest, get_test_data
from app.models import Company

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-co', nargs='+', type=str)

    def handle(self, *args, **options):
        print(options)
        codes = ['visions', 'sffire', 'uccu', 'cscu']
        if options['co']:
            codes = options['co'][0]
        kwargs = {'test_id': 'rpt', 'test_url': 'prod', 'take_screenshots': 'all', 'timeout':120}
        for code in codes:
            mode = 'file'
            key = None
            co = Company.objects.get(code=code)
            print(co)
            kwargs['co'] = co
            testd = get_test_data(co, key, mode=mode)
            print(testd)
            print(kwargs)
            #self.stdout.write(ptest(**kwargs))
            el =  ptest(**kwargs)
            #el = ptest(co, key, env, testd=testd, take_screenshots=True, wait=wait)
