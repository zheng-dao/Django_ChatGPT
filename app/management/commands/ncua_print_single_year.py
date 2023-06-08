from django.core.management.base import BaseCommand, CommandError
from file_tools import save_csv, load_csv_data, map_fields_for_data_summary
from ncua_tools import calculate_benchmark, calculate_growth_rates, get_filename, get_mapping, series_full_form, get_previous_years_data, calculate_growth, import_data
from app.models import AnalyticsPlatform, Company, DataSummary
from timedate import get_qtr
from django.db import connections

SQL_DATA_PATH = 'C:\\ProgramData\\MySQL\\MySQL Server 5.7\\Data\\ga\\'

class Command(BaseCommand):
    help = 'name of the CU '

    def add_arguments(self, parser):
        parser.add_argument('-c', '--cu_name', dest='cu_name', type=str)
        #parser.add_argument('year', type=int)
        parser.add_argument('-d', '--date_str', dest='date_str', nargs='+', type=str)
    
    def return_row(self, rows, required_field, index):
        for row in rows:
            if required_field in row:
                pass

    def handle(self, *args, **options):
        print(options)
        temp_records_dict = {}
        missing_records = []
        #import pdb;pdb.set_trace()
        period = 'quarterly'
        quarter = 'all'
        # yr, mo = options['date_str'][0].split('-')
        # qtr = get_qtr(mo)
        # default_quarters_all = DataSummary().get_period_list(period)

        qtr = ['03','06','09','12']
        fn_datasummary = get_filename('datasummary')
        fn_company = get_filename('company')
        map_dict = get_mapping('datasummary')
        map_dict ={
            'cu_number':'number',
            'acct_083':'total number of members',
            'acct_710':'total outstanding loans',
            'acct_018':'total shares and deposits',
            'acct_025a':'total number of loans and leases',
            'acct_025b':'total amount of loans and leases',
            'acct_010':'total assets (liabilities, deposits, etc)',
            }
        # series = list(map_dict.values())[1:]
        # keys = list(map_dict.keys())[1:]
        # ap = AnalyticsPlatform.objects.get(code='ncua')

        # series_to_calculate = series_full_form(period)
        # quarters_all = [quarter]
        # if quarter == 'all':
        #     quarters_all = default_quarters_all
        company_name = options['cu_name']
        list_of_company_name = company_name.split(',')
        dict_to_print = {}

        for company_name in list_of_company_name:
            company_name = company_name.upper()
            data_str = options['date_str']
            #fp = 'app/data/ncua/' + options['date_str'] + '-' + qtr[3]
            for qx in qtr:
                fp = 'app/data/ncua/' + options['date_str'][0]+ '-' + qx

                rows = load_csv_data(fn_company, fp) 
                for i, row in enumerate(rows):
                    if i == 0:
                        header = row
                        cu_name_index = header.index('CU_NAME')
                    if company_name in row[cu_name_index]:
                        final_company_name = row[cu_name_index]
                        #print(final_company_name)
                        cu_number = row[0]
                        if cu_number not in dict_to_print:
                            dict_to_print[cu_number] = {'name':final_company_name}
                        #print("Found the cu number")
                        #break
            
           
        print('Getting', len(dict_to_print.keys()), 'credit unions')
        for qx in qtr:
            fp = 'app/data/ncua/' + options['date_str'][0]+ '-' +qx
            new_row_of_datasummary = load_csv_data(fn_datasummary, fp)
            for cu_n in dict_to_print.keys():
                #print("CU Number:\t {}".format(cu_number))
                #print("Year\t\tQuarter\t\tvalue\t\tseries_name")
                #import pdb;pdb.set_trace()
                # print(qx)
                date_str = data_str[0]+'-'+qx
                #data_list = map_fields_for_data_summary(date_str, 'datasummary', get_mapping('datasummary'), new_row_of_datasummary, 'credit_union', 'quarterly')
                data_list = map_fields_for_data_summary(date_str, 'datasummary', map_dict, new_row_of_datasummary, 'credit_union', 'quarterly')
                quarter = get_qtr(qx)
                final_company_name = dict_to_print[cu_n]['name']
                dict_to_print[cu_n][quarter] = {}
                #for i, row in enumerate(new_row_of_datasummary):
                for i, data_ in enumerate(data_list):
                    if int(cu_n) == int(data_[0]['entity_id']):# and data_[0].get(quarter,0):
                            #print(data_[0]['entity_id'])
                            #import pdb;pdb.set_trace()
                            required_data = data_
                            for data_r in required_data:
                                #print(data_r)
                                year_required = data_r['year']
                            
                                series_name = data_r['series']

                            # import pdb;pdb.set_trace()
                                value = data_r.get(quarter,0)
                                dict_to_print[cu_n][quarter][series_name] = value
                                #print("{}\t\t{}\t\t{}\t\t{}".format(year_required, quarter, value, series_name.strip()))
                            #break
        #print(dict_to_print)
        for cu_n in dict_to_print.keys():
            print(dict_to_print[cu_n]['name'], year_required)
            print("{}\t{}\t{}\t{}\t{}".format('q1', 'q2', 'q3', 'q4', 'series'))
            for s in dict_to_print[cu_n]['q1'].keys():
                d = dict_to_print[cu_n]
                print("{}\t{}\t{}\t{}\t{}".format(d['q1'][s], d['q2'][s], d['q3'][s], d['q4'][s], s))


