from django.core.management.base import BaseCommand, CommandError
from file_tools import save_csv, load_csv_data
from ncua_tools import calculate_benchmark, calculate_growth_rates, get_filename, get_mapping, series_full_form, get_previous_years_data, calculate_growth, import_data, get_derivatives, files
from app.models import AnalyticsPlatform, Company, DataSummary, Tier
from timedate import get_qtr
from django.db import connections
from django.forms.models import model_to_dict
from django.db.models import Avg
from django.conf import settings

#SQL_DATA_PATH = 'C:\\ProgramData\\MySQL\\MySQL Server 5.7\\Data\\ga\\'
SQL_DATA_PATH = settings.SQL_DATA_PATH
SQL_DB_NAME = settings.SQL_DB_NAME

def operate(d_operate, data):
    #print(d_operate)
    #print(data)
    for i, action in enumerate(d_operate['operations']):
        if d_operate['data'][i] in data and d_operate['data'][i+1] in data:
            if action == '/' and float(data[d_operate['data'][i+1]]) and data[d_operate['data'][i]]:
                return float(data[d_operate['data'][i]])/float(data[d_operate['data'][i+1]])
            else:
                return 0

class Command(BaseCommand):
    help = 'import the latest quarter of NCUA data (raw_import ncua 2019-03). Optionally add a # of records: ncua_import ncua 2019-03 3 (for 3 records imported)'

    def add_arguments(self, parser):
        parser.add_argument('date_str', nargs='+', type=str)

    def handle(self, *args, **options):
        print(options)
        platform_code = options['date_str'][0]
        date_str = options['date_str'][1]
        entity_type = 'credit_union'
        date_in_filename = delimiter = None
        data_start_row = 1
        num_records = 10000000
        if len(options['date_str']) == 3:
            num_records = int(options['date_str'][2]) + 1
        if platform_code == 'fdic':
            #from fdic_tools import get_filename, get_mapping, import_data
            entity_type = 'bank'
            delimiter = '\t'
            date_in_filename = date_str
            data_start_row = 2
            num_records += 1
        print(platform_code, date_str, entity_type, num_records)

        create = ['base_data', 'state']
        create = ['base_data', platform_code, 'derivatives', 'benchmarks', 'growth', 'state', 'derivatives_growth']
        #create = ['base_data', platform_code, 'derivatives', 'benchmarks', 'state']
        #create = [platform_code, 'growth', 'derivatives_growth']
        growth = {}
        growth = {'prefix':['Average'], 'suffix':['quarterly growth', 'year over year', 'quarter over quarter']}
        growth = {'suffix':['quarterly growth', 'year over year', 'quarter over quarter']}
        derivative = get_derivatives()
        #derivative = {'ncua':{
        #    'assets per member':{
        #        'data':['total assets (liabilities, deposits, etc)', 'total number of members'], 
        #        'operations':['/']},
        #    'average loan amount':{
        #        'data':['total amount of loans and leases', 'total number of loans and leases'], 
        #        'operations':['/']},
        #    'shares and deposits per member':{
        #        'data':['total shares and deposits', 'total number of members'], 
        #        'operations':['/']},
        #    'number of loans per member':{
        #        'data':['total number of loans and leases', 'total number of members'], 
        #        'operations':['/']},
        #    }}
        #derivative = {'ncua':{
        #    'assets per member':{
        #        'data':['total assets (liabilities, deposits, etc)', 'total number of members'], 
        #        'operations':['/']},
        #    }}
        yr, mo = options['date_str'][1].split('-')
        temp_records_dict = {}
        missing_records = []
        period = 'quarterly'
        quarter = 'all'
        qtr = get_qtr(mo)
        default_quarters_all = DataSummary().get_period_list(period)
        map_dict = get_mapping('datasummary')
        #print(map_dict)
        series = list(map_dict.values())[1:]
        keys = list(map_dict.keys())[1:]
        ap = AnalyticsPlatform.objects.get(code=platform_code)

        series_to_calculate = series_full_form(period)
        quarters_all = [quarter]
        if quarter == 'all':
            quarters_all = default_quarters_all
        rows = []
        h = []
        hl = []
        len_rows = 0
        for key, val in files.items():
            if not key in ['fs220l', 'fs220m'] or int(yr) > 2017:
                print(key, val)
                #fn = get_filename('datasummary', date_in_filename)
                fp = 'app/data/' + platform_code + '/' + options['date_str'][1]
                try:
                    row_temp = load_csv_data(key + '.txt', fp, delimiter=delimiter)
                except:
                    try:
                        row_temp = load_csv_data(key.upper() + '.txt', fp, delimiter=delimiter)
                    except:
                        row_temp = load_csv_data(key.lower()[:-1] + key[-1:].upper()  + '.txt', fp, delimiter=delimiter)
                if len_rows == 0:
                    rows = row_temp
                    h = row_temp[0]
                    len_rows += len(row_temp[0])
                    #print('h ', len(h), 'r ', len(rows[0]), 'rt ', len(row_temp[0]), 'lenrows', len_rows)
                else:
                    h += row_temp[0]
                    rlen = len(row_temp[0])
                    for j, r in enumerate(rows):
                        if j != 0:
                            if rows[j][0] == row_temp[j][0]:
                                rows[j] += row_temp[j]
                            else:
                                rows[j] += [0]*rlen
                    len_rows += len(row_temp[j])
                    #print('h ', len(h), 'r ', rlen, 'rt ', len(row_temp[j]), 'lenrows', len_rows)
                #print(len_rows)
            hl = [x.lower() for x in h]
            #print(hl)

        #h = rows[0]
        #hl = [x.lower() for x in h]
        #print(hl)
        field_list = ['entity_id', 'entity_type', 'series', 'series_id', 'custom', 'series_type', 'year', 'analyticsplatform_id', 'base_data_interval', 'state']
        print('generating csvs in mysql default data directory')
        for_derivative = {}

        companies = dict(Company.objects.values_list('number', 'state').filter(company_type='credit_union'))

        for i,m in enumerate(map_dict):
            outrows=[]
            #print(i, m)
            for j, row in enumerate(rows[data_start_row:num_records]):
                #print(j, row[0])
                #if j != 0:
                id = row[0]
                if 'derivatives' in create or 'derivatives_growth' in create:
                    if not id in for_derivative:
                        for_derivative[id] = {}
                    if m in hl and m in map_dict:
                        #print(id, m)
                        #print(for_derivative[id])
                        #print(map_dict[m])
                        #print(len(row))
                        #print(len(hl))
                        #print('len rows', len_rows)
                        #print(hl.index(m))
                        for_derivative[id][map_dict[m]] = row[hl.index(m)]
                        state = companies.get(id)
                        outrows.append([id, entity_type, map_dict[m], m, row[hl.index(m)], 'raw', yr, ap.id, period, state])
            save_csv(outrows, field_list, fn=map_dict[m]+'.csv', fp=SQL_DATA_PATH)

        #if 'base_data' not in create:
        #    series = []
        if ('derivatives' in create  or 'derivatives_growth' in create) and platform_code in derivative:
            if platform_code not in create:
                series = []
            for s, d_operate in derivative[platform_code].items():
                outrows=[]
                series.append(s)
                keys.append(s)
                for id, data in for_derivative.items():
                    derived = operate(d_operate, data)
                    state = companies.get(id)
                    outrows.append([id, entity_type, s, s, derived, 'raw', yr, ap.id, period, state])
                save_csv(outrows, field_list, fn=s+'.csv', fp=SQL_DATA_PATH)

        if 'base_data' in create or 'derivatives' in create:
            with connections['default'].cursor() as cursor:
                print('STARTING IMPORT PROCESS')
                for i,s in enumerate(series):
                    print(i, s, yr, qtr)
                    #outrows=[]
                    #m = keys[i]
                    #for j, row in enumerate(rows):
                    #    if j != 0:
                    #        outrows.append([row[0], 'credit_union', map_dict[m], m, row[hl.index(m)], yr, ap.id, 'quarterly'])
                    #save_csv(outrows, field_list, fn=map_dict[m]+'.csv', fp=SQL_DATA_PATH)
                    if qtr == 'q1':
                        #sql = "CREATE TABLE " + SQL_DB_NAME + "temp LIKE " + SQL_DB_NAME + "app_datasummary;"
                        sql = "DELETE FROM " + SQL_DB_NAME + "temp;"
                        cursor.execute(sql)
                        print('temp table records deleted')
                        sql = ('%s%s%s%s%s')%("LOAD DATA INFILE '", s + '.csv' + "'", ' INTO TABLE ', SQL_DB_NAME, """temp FIELDS TERMINATED by ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS (entity_id,entity_type,series,series_id,custom,series_type,year,analyticsplatform_id,base_data_interval,state);""")
                        #print(sql)
                        cursor.execute(sql)
                        print('data imported to temp table')
                        #if qtr == 'q1':
                            #sql = ('%s%s%s')%("LOAD DATA INFILE '", s + '.csv', "'INTO TABLE " + SQL_DB_NAME + "app_datasummary FIELDS TERMINATED by ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS (entity_id,entity_type,series,series_id,custom,year);")
                            #sql = ('%s%s%s')%("LOAD DATA INFILE '", s + '.csv', """' INTO TABLE " + SQL_DB_NAME + "app_datasummary FIELDS TERMINATED by ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS (entity_id,entity_type,series,series_id,custom,year);""")
                        sql = "UPDATE " + SQL_DB_NAME + "temp SET " + SQL_DB_NAME + "temp."+ qtr + " = " + SQL_DB_NAME + "temp.custom+0.0, " + SQL_DB_NAME + "temp.custom=NULL, " + SQL_DB_NAME + "temp.analyticsplatform_id=" + str(ap.id) + ", " + SQL_DB_NAME + "temp.base_data_interval='quarterly';"
                        cursor.execute(sql)
                        print('update', qtr, 'with custom')

                        #sql = "UPDATE " + SQL_DB_NAME + "app_datasummary INNER JOIN " + SQL_DB_NAME + "temp on " + SQL_DB_NAME + "temp.entity_id = " + SQL_DB_NAME + "app_datasummary.entity_id INNER JOIN " + SQL_DB_NAME + "temp as a on a.series_id = " + SQL_DB_NAME + "app_datasummary.series_id INNER JOIN " + SQL_DB_NAME + "temp as b on b.year = " + SQL_DB_NAME + "app_datasummary.year INNER JOIN " + SQL_DB_NAME + "temp as c on c.analyticsplatform_id = " + SQL_DB_NAME + "app_datasummary.analyticsplatform_id SET " + SQL_DB_NAME + "app_datasummary."+ qtr + " = " + SQL_DB_NAME + "temp.custom;"
                        sql = "INSERT INTO " + SQL_DB_NAME + "app_datasummary (entity_id,entity_type,series,series_id," + qtr + ",series_type,year, analyticsplatform_id, base_data_interval,state) SELECT entity_id,entity_type,series,series_id," + qtr + ",series_type,year, analyticsplatform_id+0, base_data_interval, state from " + SQL_DB_NAME + "temp;"
                        #print(sql)
                        cursor.execute(sql)
                        print('DataSummary ', qtr, ' field updated with temp table data from temp')

                        #sql = "DROP TABLE " + SQL_DB_NAME + "temp;"
                        sql = "DELETE FROM " + SQL_DB_NAME + "temp;"
                        cursor.execute(sql)
                        print('temp table records deleted')
                    else:
                        bulk = []
                        records = DataSummary.objects.filter(analyticsplatform=ap, year=int(yr), series=s, entity_type=entity_type, entity_subtype=None).values()
                        print(records.count())
                        if records:
                            for r in records:
                                temp_records_dict[r['entity_id']] = r
                            if s in derivative[platform_code]:
                                hindex = 4
                                rows = load_csv_data(s + '.csv', SQL_DATA_PATH, delimiter=delimiter)
                            else:
                                hindex = hl.index(r['series_id'])
                            for i, row in enumerate(rows[data_start_row:num_records]):
                                if int(row[0]) in temp_records_dict:
                                    temp_records_dict[int(row[0])][qtr] = None
                                    if row[hindex]:
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
            print('CALCULATING BENCHMARKS')
            print(series)
            kwargs = {}
            kwargs['analyticsplatform'] = ap
            kwargs['year'] = int(yr)
            kwargs['entity_type'] = entity_type
            kwargs['base_data_interval'] = period
            kwargs['series'] = s
            kwargs['entity_subtype'] = None

            #calculate asset tier benchmarks
            s = 'total assets (liabilities, deposits, etc)'
            print('querying entity IDs for each tier benchmark from total assets')
            qtr = get_qtr(mo)
            tiers = Tier.objects.all().order_by('tier')
            tier_entity_ids = {}
            for j,t in enumerate(tiers):
                print('tier ', str(j+1))
                ds = DataSummary.objects.filter(analyticsplatform=ap, year=int(yr), entity_type='benchmark', series=s, entity_subtype='tier', entity_subtype_id=str(j+1)).first()
                kwargs['series'] = s
                for tqtr in default_quarters_all:
                    kwargs.pop(tqtr + '__gte', None)
                    kwargs.pop(tqtr + '__gt', None)
                    kwargs.pop(tqtr + '__lte', None)
                    kwargs.pop(tqtr + '__lt', None)
                if j == 0:
                    kwargs[qtr + '__lte'] = t.max_assets
                elif j == len(tiers) - 1:
                    kwargs[qtr + '__gt'] = t.min_assets
                else:
                    kwargs[qtr + '__gt'] = t.min_assets
                    kwargs[qtr + '__lte'] = t.max_assets
                #print(kwargs)
                records = DataSummary.objects.filter(**kwargs).values_list('id', flat=True)
                tier_entity_ids[t.tier] = list(records)


            print('calculating tier benchmarks')
            for i,s in enumerate(series):
                for j,t in enumerate(tiers):
                    kwargs['series'] = s
                    for tqtr in default_quarters_all:
                        kwargs.pop(tqtr + '__gte', None)
                        kwargs.pop(tqtr + '__gt', None)
                        kwargs.pop(tqtr + '__lte', None)
                        kwargs.pop(tqtr + '__lt', None)

                    records = DataSummary.objects.filter(**kwargs).values_list(qtr, flat=True)
                    #print(len(records))
                    avg = calculate_benchmark(records, 'avg')
                    ds = DataSummary.objects.filter(analyticsplatform=ap, year=int(yr), entity_type='benchmark', series=s, entity_subtype='tier', entity_subtype_id=t.tier).first()
                    if ds:
                        setattr(ds, qtr, avg)
                    else:
                        tierd = kwargs.copy()
                        tierd.pop('q1', None)
                        tierd.pop('q2', None)
                        tierd.pop('q3', None)
                        tierd.pop('q4', None)
                        tierd.pop(qtr + '__gt', None)
                        tierd.pop(qtr + '__lte', None)
                        tierd.pop(qtr + '__lt', None)
                        tierd.pop('entity_id', None)
                        tierd['series'] = s
                        tierd['entity_type'] = 'benchmark'
                        tierd['series_id'] = keys[i] + '__' + str(j + 1)
                        tierd['series_type'] = 'average'
                        tierd['entity_subtype'] = 'tier'
                        tierd['entity_subtype_id'] = t.tier
                        tierd[qtr] = avg
                        #print(tierd)
                        ds = DataSummary(**tierd)
                    ds.save()
                print(s, 'tier record written')

            #CALC NORMAL BENCHMARKS
            for i,s in enumerate(series):
                ds = None
                kwargs = {}
                kwargs['analyticsplatform'] = ap
                kwargs['year'] = int(yr)
                kwargs['entity_type'] = entity_type
                kwargs['base_data_interval'] = period
                kwargs['series'] = s
                kwargs['entity_subtype'] = None
                ds = DataSummary.objects.filter(analyticsplatform=ap, year=int(yr), entity_type='benchmark', series=s, entity_subtype='country', entity_subtype_id='US').first()
            #for j, tqtr in enumerate(default_quarters_all):
                print(s, yr, qtr)
                field = qtr + '__gt'
                kwargs[field] = 0
                print('querying')
                records = DataSummary.objects.filter(**kwargs).values_list(qtr, flat=True)
                avg = calculate_benchmark(records, 'avg')
                #if tqtr == 'q1':
                if not ds:
                    #if j == 0:
                    d = kwargs.copy()
                    d['series'] = s
                    d['series_id'] = keys[i]
                    d['series_type'] = 'average'
                    d['entity_type'] = 'benchmark'
                    d['entity_subtype'] = 'country'
                    d['entity_subtype_id'] = 'US'
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
                #    setattr(ds, tqtr, avg)
                ds.save()


        if 'state' in create:
            print('-----------------------------------')
            #print('updating DS state field for each credit union...querying entity_ids for the state')
            #states = Company.objects.order_by('state').values_list('state', flat=True).distinct()
            #for state in states:
            #    if state and state not in ['0', '0 ']:
            #        print(state)
            #        entity_ids = Company.objects.values_list('number', flat=True).filter(state=state, company_type=entity_type)
            #        print('updating states data in DS')
            #        dss = DataSummary.objects.filter(analyticsplatform=ap, entity_type='credit_union', entity_id__in=entity_ids, entity_subtype=None, state=None)
            #        for ds in dss:
            #            ds.state = state
            #            ds.save()

            print('CALCULATING STATE BENCHMARKS', yr, qtr)
            for i,s in enumerate(series):
                #state_data = []
                #ids_to_delete = []
                ds_list = []
                kwargs = {}
                kwargs['analyticsplatform'] = ap
                kwargs['year'] = int(yr)
                kwargs['entity_type'] = entity_type
                kwargs['base_data_interval'] = period
                kwargs['series'] = s
                kwargs['entity_subtype'] = None
                kwargs[qtr + '__gt'] = 0
                print('querying states to annotate')
                ds = DataSummary.objects.filter(**kwargs)
                states = ds.values('state').annotate(Avg(qtr))
                statesd = {}
                for stated in states:
                    statesd[stated['state']] = stated[qtr + '__avg']

                kwargs.pop(qtr + '__gt', None)
                kwargs['entity_type'] = 'benchmark'
                kwargs['entity_subtype'] = 'state'
                print('querying current benchmarks if there are any for this year')
                dss = DataSummary.objects.filter(**kwargs)
                if dss:
                    for dsd in dss.values():
                        state = dsd['state']
                        #print(state)
                        if state and state not in ['0', '0 ']:
                            if state in statesd:
                                dsd[qtr] = statesd[state]
                            dsd.pop('id', None)
                            ds_list.append(DataSummary(**dsd))
                else:
                    for state, avg in statesd.items():
                        if state and state not in ['0', '0 ']:
                            d = kwargs.copy()
                            d['series'] = s
                            d['series_id'] = keys[i] + '_' + state
                            d['series_type'] = 'average'
                            d['entity_type'] = 'benchmark'
                            d['entity_subtype'] = 'state'
                            d['entity_subtype_id'] = state
                            d['state'] = state
                            #print(qtr)
                            d[qtr] = avg
                            ds_list.append(DataSummary(**d))
                print('start delete for states:', s)
                if dss:
                    print(dss.delete())
                print('start bulk create for states:', s)
                if ds_list:
                    DataSummary.objects.bulk_create(ds_list, 1000)

        if 'growth' in create or 'derivatives_growth' in create:
            series_adapted = series
            print('CALCULATING GROWTH FOR', series_adapted)
            calculate_growth_rates(year=int(yr), quarter=qtr, period=period, series=series_adapted)
            #for k, v in growth.items():
            #    for appendage in v:
            #        series_adapted = []
            #        if k == 'prefix':
            #            series_adapted = [appendage + ' ' + s for s in series]
            #        elif k == 'suffix':
            #            series_adapted = [s + ' ' + appendage for s in series]
            #        print('-----------------------------------')
            #        print('starting to calculate growth rates for quarter', qtr)
            #        print(series_adapted)
            #        calculate_growth_rates(year=int(yr), quarter=qtr, period=period, series=series_adapted)
