from django.core.management.base import BaseCommand, CommandError
from file_tools import save_csv, load_csv_data
from ncua_tools import calculate_benchmark, calculate_growth_rates, get_filename, get_mapping, series_full_form, get_previous_years_data, calculate_growth, import_data
from app.models import AnalyticsPlatform, Company, DataSummary
from timedate import get_qtr
from django.db import connections
from django.conf import settings

#SQL_DATA_PATH = 'C:\\ProgramData\\MySQL\\MySQL Server 5.7\\Data\\ga\\'
SQL_DATA_PATH = settings.SQL_DATA_PATH

def operate(d):
    for i, action in enumerate(d['operations'].items()):
        if action == '/':
            return d['data'][i]/d['data'][i+1]

class Command(BaseCommand):
    help = 'import the latest quarter of NCUA data (ncua_import 2019-03). Optionally add a # of records: ncua_import 2019-03 2 (for 2 records imported)'

    def add_arguments(self, parser):
        parser.add_argument('date_str', nargs='+', type=str)

    def handle(self, *args, **options):
        print(options)
        create = ['ncua', 'benchmarks']#, 'growth']
        create = ['state']
        #create = ['ncua', 'benchmarks', 'state', 'growth']
        #growth = {'prefix':['Average'], 'suffix':['quarterly growth', 'year over year', 'quarter over quarter']}
        growth = {'prefix':['Average']}
        derivative = {
            'Assets/member':{
                'data':['total number of members', 'total assets (liabilities, deposits, etc)'], 
                'operations':['/']},
            'Average loan amount':{
                'data':['total amount of loans and leases', 'total number of loans and leases'], 
                'operations':['/']},
            'Shares and deposits/member':{
                'data':['total shares and deposits', 'total number members'], 
                'operations':['/']},
            'Number of loans/member':{
                'data':['total number of loans and leases', 'total number of members'], 
                'operations':['/']},
            }
        temp_records_dict = {}
        missing_records = []
        period = 'quarterly'
        quarter = 'all'
        yr, mo = options['date_str'][0].split('-')
        num_records = 10000000
        if len(options['date_str']) == 2:
            num_records = int(options['date_str'][1]) + 1
        qtr = get_qtr(mo)
        default_quarters_all = DataSummary().get_period_list(period)
        fn = get_filename('datasummary')
        map_dict = get_mapping('datasummary')
        series = list(map_dict.values())[1:]
        keys = list(map_dict.keys())[1:]
        ap = AnalyticsPlatform.objects.get(code='ncua')

        series_to_calculate = series_full_form(period)
        quarters_all = [quarter]
        if quarter == 'all':
            quarters_all = default_quarters_all
        fp = 'app/data/ncua/' + options['date_str'][0]
        rows = load_csv_data(fn, fp) 
        h = rows[0]
        hl = [x.lower() for x in h]
        field_list = ['entity_id', 'entity_type', 'series', 'series_id', 'custom', 'year', 'analyticsplatform_id', 'base_data_interval']
        print('generating csvs in mysql default data directory')
        for i,m in enumerate(map_dict):
            outrows=[]
            for_derivative = {}
            #print(i, m)
            for j, row in enumerate(rows[:num_records]):
                #print(j, row[0])
                if j != 0:
                    id = row[0]
                    if map_dict[m] not in for_derivative:
                        for_derivative[map_dict[m]] = {}
                    for_derivative[map_dict[m]][id] = row[hl.index(m)]
                    outrows.append([id, 'credit_union', map_dict[m], m, row[hl.index(m)], yr, ap.id, 'quarterly'])
            save_csv(outrows, field_list, fn=map_dict[m]+'.csv', fp=SQL_DATA_PATH)

        if 'ncua' in create:
            if 'derivatives' in create:
                for series, data in derivative.items():
                    outrows=[]
                    for id, d in data.items():
                        derived = operate(d)
                        outrows.append([id, 'credit_union', series, series, derived, yr, ap.id, 'quarterly'])
                    save_csv(outrows, field_list, fn=series+'.csv', fp=SQL_DATA_PATH)

            with connections['default'].cursor() as cursor:
                print('starting import process')
                for i,s in enumerate(series):
                    print(s, yr, qtr)
                    #outrows=[]
                    #m = keys[i]
                    #for j, row in enumerate(rows):
                    #    if j != 0:
                    #        outrows.append([row[0], 'credit_union', map_dict[m], m, row[hl.index(m)], yr, ap.id, 'quarterly'])
                    #save_csv(outrows, field_list, fn=map_dict[m]+'.csv', fp=SQL_DATA_PATH)
                    if qtr == 'q1':
                        #sql = "CREATE TABLE ga.temp LIKE ga.app_datasummary;"
                        sql = "DELETE FROM ga.temp;"
                        cursor.execute(sql)
                        print('temp table records deleted')
                        sql = ('%s%s%s')%("LOAD DATA INFILE '", s + '.csv', """'INTO TABLE ga.temp FIELDS TERMINATED by ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS (entity_id,entity_type,series,series_id,custom,year,analyticsplatform_id,base_data_interval);""")
                        cursor.execute(sql)
                        print('data imported to temp table')
                        #if qtr == 'q1':
                            #sql = ('%s%s%s')%("LOAD DATA INFILE '", s + '.csv', "'INTO TABLE ga.app_datasummary FIELDS TERMINATED by ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS (entity_id,entity_type,series,series_id,custom,year);")
                            #sql = ('%s%s%s')%("LOAD DATA INFILE '", s + '.csv', """' INTO TABLE ga.app_datasummary FIELDS TERMINATED by ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS (entity_id,entity_type,series,series_id,custom,year);""")
                        sql = "UPDATE ga.temp SET ga.temp."+ qtr + " = ga.temp.custom+0.0, ga.temp.custom=NULL, ga.temp.analyticsplatform_id=" + str(ap.id) + ", ga.temp.base_data_interval='quarterly';"
                        cursor.execute(sql)
                        print('update', qtr, 'with custom')

                        #sql = "UPDATE ga.app_datasummary INNER JOIN ga.temp on ga.temp.entity_id = ga.app_datasummary.entity_id INNER JOIN ga.temp as a on a.series_id = ga.app_datasummary.series_id INNER JOIN ga.temp as b on b.year = ga.app_datasummary.year INNER JOIN ga.temp as c on c.analyticsplatform_id = ga.app_datasummary.analyticsplatform_id SET ga.app_datasummary."+ qtr + " = ga.temp.custom;"
                        sql = "INSERT INTO ga.app_datasummary (entity_id,entity_type,series,series_id," + qtr + ",year, analyticsplatform_id, base_data_interval) SELECT entity_id,entity_type,series,series_id," + qtr + ",year, analyticsplatform_id+0, base_data_interval from ga.temp;"
                        print(sql)
                        cursor.execute(sql)
                        print('DataSummary ', qtr, ' field updated with temp table data from temp')

                        #sql = "DROP TABLE ga.temp;"
                        sql = "DELETE FROM ga.temp;"
                        cursor.execute(sql)
                        print('temp table records deleted')
                    else:
                        bulk = []
                        records = DataSummary.objects.filter(analyticsplatform=ap, year=int(yr), series=s, entity_type='credit_union').values()
                        print(records.count())
                        for r in records:
                            temp_records_dict[r['entity_id']] = r
                        hindex = hl.index(r['series_id'])
                        for i, row in enumerate(rows[:num_records]):
                            if i != 0 and int(row[0]) in temp_records_dict:
                                temp_records_dict[int(row[0])][qtr] = row[hindex]
                                bulk.append(DataSummary(**temp_records_dict[int(row[0])]))
                            else:
                                missing_records.append(row)
                                #print('this records did not exist')
                                #print(row)
                        print('starting records delete')
                        ids=list(records.values_list('id', flat=True))
                        DataSummary.objects.filter(id__in=ids).delete()
                        print('records deleted')
                        DataSummary.objects.bulk_create(bulk, 1000)
                        print('records re-added')

        if missing_records:
            #print(missing_records)
            print('There were some missing records----------------------------------------')
            print(len(missing_records))
            print('--------------------------------------------------------------------------------')

        if 'benchmarks' in create:
            print('-----------------------------------')
            print('calculating benchmarks')
            for i,s in enumerate(series):
                ds = None
                kwargs = {}
                kwargs['analyticsplatform'] = ap
                kwargs['year'] = int(yr)
                kwargs['entity_type'] = 'credit_union'
                kwargs['base_data_interval'] = 'quarterly'
                kwargs['series'] = s
                ds = DataSummary.objects.filter(analyticsplatform=ap, year=int(yr), entity_type='benchmark', series = 'Average ' + s).first()
                for j, qtr in enumerate(default_quarters_all):
                    print(s, yr, qtr)
                    field = qtr + '__gt'
                    kwargs[field] = 0
                    print('querying')
                    records = DataSummary.objects.filter(**kwargs).values_list(qtr, flat=True)
                    avg = calculate_benchmark(records, 'avg')
                    #if qtr == 'q1':
                    if not ds:
                        #if j == 0:
                        d = kwargs.copy()
                        d['series'] = 'Average ' + s
                        d['series_id'] = keys[i]
                        d['entity_type'] = 'benchmark'
                        d[qtr] = avg
                        d.pop('q1__gt', None)
                        d.pop('q2__gt', None)
                        d.pop('q3__gt', None)
                        d.pop('q4__gt', None)
                        d.pop('entity_id', None)
                        ds = DataSummary(**d)
                    elif ds:
                        #ds = DataSummary.objects.get(analyticsplatform=ap, year=int(yr), entity_type='benchmark', series = 'Average ' + s)
                        setattr(ds, qtr, avg)
                    #else:
                    #    setattr(ds, qtr, avg)
                ds.save()
                print('record written')

        if 'state' in create:
            print('-----------------------------------')
            print('calculating state benchmarks')
            states = Company.objects.order_by('state').values_list('state', flat=True).distinct()
            for i,s in enumerate(series):
                state_data = []
                ids_to_delete = []
                for state in states:
                    ds = None
                    if state:
                        entity_ids = Company.objects.values_list('number', flat=True).filter(state=state)
                        kwargs = {}
                        kwargs['entity_id__in'] = entity_ids
                        kwargs['analyticsplatform'] = ap
                        kwargs['year'] = int(yr)
                        kwargs['entity_type'] = 'credit_union'
                        kwargs['base_data_interval'] = 'quarterly'
                        kwargs['series'] = s
                        #for j, qtr in enumerate(default_quarters_all):
                        print(state, s, yr, qtr)
                        field = qtr + '__gt'
                        kwargs[field] = 0
                        print('querying')
                        records = DataSummary.objects.filter(**kwargs).values_list(qtr, flat=True)
                        avg = calculate_benchmark(records, 'avg')
                        if qtr == 'q1':
                            #if j == 0:
                            d = kwargs.copy()
                            d['series'] = state + ' Average ' + s
                            d['series_id'] = keys[i] + '_' + state
                            d['entity_type'] = 'benchmark'
                            d[qtr] = avg
                            d.pop('q1__gt', None)
                            d.pop('q2__gt', None)
                            d.pop('q3__gt', None)
                            d.pop('q4__gt', None)
                            d.pop('entity_id', None)
                            d.pop('entity_id__in', None)
                            ds = DataSummary(**d)
                        else:
                            ds = DataSummary.objects.get(analyticsplatform=ap, year=int(yr), entity_type='benchmark', series = state + ' Average ' + s)
                            ids_to_delete.append(ds.id)
                            setattr(ds, qtr, avg)
                            setattr(ds, 'id', None)
                            ds.pk = None
                        #else:
                        #    setattr(ds, qtr, avg)
                        #    setattr(ds, 'id', None)
                        #    ds.pk = None
                        #    ids_to_delete.append(ds.id)
                        state_data.append(ds)
                    #ds.save()
                print('start delete for states:', s, len(ids_to_delete))
                DataSummary.objects.filter(id__in=ids_to_delete).delete()
                print('start bulk update for states:', s)
                DataSummary.objects.bulk_create(state_data, 1000)

        if 'growth' in create:
            for k, v in growth.items():
                for appendage in v:
                    series_adapted = []
                    if k == 'prefix':
                        series_adapted = [appendage + ' ' + s for s in series]
                    else:
                        series_adapted = [s + ' ' + appendage for s in series]
                    print('-----------------------------------')
                    print('starting to calculate growth rates for quarter', qtr)
                    print(series_adapted)
                    calculate_growth_rates(year=int(yr), quarter=qtr, period=period, series=series_adapted)
