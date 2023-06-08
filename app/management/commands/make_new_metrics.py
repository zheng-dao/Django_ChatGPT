from django.core.management.base import BaseCommand, CommandError
from app.models import AnalyticsPlatform, Company, DataSummary, Metric
from ncua_tools import get_mapping, get_derivatives, series_full_form

class Command(BaseCommand):
    help = 'do various calculations'

    def add_arguments(self, parser):
        parser.add_argument('ap', nargs='?', type=str)
        parser.add_argument('-n', '--name', type=str)

    def handle(self, *args, **options):
        print(options)
        period = 'quarterly'
        derivative = get_derivatives()
        metrics = ['states', 'benchmarks', 'growth']
        default_quarters_all = DataSummary().get_period_list(period)
        list_for_growth = []
        if options['ap'] == 'ncua':
            name = options['name']
            ap = AnalyticsPlatform.objects.get(code=options['ap'])
            m = {
                'name':name,
                'label':name,
                'analyticsplatform':ap,
            }
            metric, created = Metric.objects.get_or_create(name=m['name'], analyticsplatform=ap, defaults=m)

            ap_fin = AnalyticsPlatform.objects.get(code='fin')
            if 'states' in metrics:
                states = Company.objects.order_by('state').values_list('state', flat=True).distinct()
                for s in states:
                    if s and s != '0':
                        temp = m.copy()
                        temp['name'] = s + ' Average ' + metric.name
                        temp['label'] = temp['name']
                        temp['code'] = s
                        temp['unit'] = '#'
                        temp['subtype'] = 'state'
                        temp['analyticsplatform'] = ap_fin
                        temp['is_benchmark'] = True
                        temp['is_derivative'] = True
                        state_metric, created = Metric.objects.get_or_create(name=temp['name'], analyticsplatform=ap, defaults=temp)
                        list_for_growth.append(state_metric)

            if 'benchmarks' in metrics:
                temp = m.copy()
                temp['name'] = 'Average ' + metric.name
                temp['label'] = temp['name']
                temp['unit'] = '#'
                temp['analyticsplatform'] = ap_fin
                temp['is_benchmark'] = True
                temp['is_derivative'] = True

                bmetric, created = Metric.objects.get_or_create(name=temp['name'], analyticsplatform=ap, defaults=temp)
                list_for_growth.append(bmetric)

            if 'growth' in metrics:
                growth_to_calculate = series_full_form(period)
                for a, g in growth_to_calculate.items():
                    temp = m.copy()
                    temp['name'] = metric.name + ' ' + g
                    temp['label'] = temp['name'][0].upper() + temp['name'][1:]
                    temp['unit'] = '%'
                    temp['subtype'] = 'growth'
                    temp['analyticsplatform'] = ap
                    gmetric, created = Metric.objects.get_or_create(name=temp['name'], analyticsplatform=ap, defaults=temp)



