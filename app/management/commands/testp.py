from django.core.management.base import BaseCommand
from pmodels import ptest, get_test_data
from app.models import Company

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-co', nargs='+', type=str)
        parser.add_argument('-to', type=int)
        parser.add_argument('-mode', type=str, default='file') #db|file
        parser.add_argument('-screenshots', default=True) #db|file

    def handle(self, *args, **options):
        print(options)
        kwargs = {}
        code = options['co'][0]
        kwargs['timeout'] = options['to']
        mode = options['mode']
        key = None
        env = 'stg'
        if len(options['co']) > 1:
            #local, stg, prod
            env = options['co'][1]
        if len(options['co']) > 2:
            key = options['co'][2]
            if key in ['none', 'None']:
                key = None
        kwargs['test_id'] = key
        kwargs['test_url'] = env
        co = Company.objects.get(code=code)
        print(co)
        kwargs['co'] = co
        kwargs['take_screenshots'] = options['screenshots']
        testd = get_test_data(co, key, mode=mode)
        print(testd)
        print(kwargs)
        #self.stdout.write(ptest(**kwargs))
        el =  ptest(**kwargs)
        #el = ptest(co, key, env, testd=testd, take_screenshots=True, wait=wait)
