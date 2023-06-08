'''
Scrapes the rates for a given year and quarter on a page that looks like this:
https://www.ncua.gov/analysis/cuso-economic-data/credit-union-bank-rates/credit-union-and-bank-rates-2020-q4
'''

import requests
from lxml import html
from app.models import Rate
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'scrapes the rates for 2019-q4 so that it will look for new )'

    # This url were given in the example so used for testing
    home_url = 'https://www.ncua.gov/analysis/cuso-economic-data/credit-union-bank-rates'
    test_url = 'https://www.ncua.gov/analysis/cuso-economic-data/credit-union-bank-rates/credit-union-and-bank-rates-2020-q4'
    best_url = 'https://www.ncua.gov'

    def add_arguments(self, parser):
        parser.add_argument('date_str', nargs='?', type=str)

    def handle(self, *args, **options):
        print("The options are ::",options)
        quarter_arguments = options.get('date_str')
        if quarter_arguments is None:
            quarter_arguments = self.get_latest_data()
        
        print("Looking for the quarter arguments", quarter_arguments)
        html_page = self.get_html_page(self.home_url)
        total_quarter_links = html_page.xpath('//h2[contains(text(),"Economic Data")]/parent::div/div/ul/li//@href')
        total_quarter_data = [td.split('rates-')[-1] for td in total_quarter_links]
        upto_date = total_quarter_data.index(quarter_arguments)
        entity_types = ['credit_union', 'bank']
        start_row = 0
        if upto_date:
            list_of_links = total_quarter_links[start_row:upto_date+1]
            list_of_quarters = total_quarter_data[start_row:upto_date+1]
            for i, url_link in enumerate(list_of_links):
                html_page = self.get_html_page(url_link)
                table_details = self.parse_table(html_page)
            
                year, quarter = list_of_quarters[i].split('-')[0], list_of_quarters[i].split('-')[1]
                
                print('Year it is looking for ', year)
                print('Quarter it is looking for', quarter)
                for datas in table_details:
                    product = datas['product']
            list_of_links = total_quarter_links[start_row:upto_date]
            list_of_quarters = total_quarter_data[start_row:upto_date]
            for i, url_link in enumerate(list_of_links):
                html_page = self.get_html_page(url_link)
                table_details = self.parse_table(html_page)
                year, quarter = list_of_quarters[i].split('-')[0], list_of_quarters[i].split('-')[1]
                print(year, quarter)
                for data in table_details:
                    product = data['product']
                    for entity_type in entity_types:
                        d = {}
                        d[quarter] = data[entity_type]
                        d['entity_type'] = entity_type
                        c, created = Rate.objects.update_or_create(product=product, entity_type=entity_type, year=year, defaults=d)
                        print("Rate dict ::", d)
                    print("Result is ", created)
        else:
            print('It is up to date')

        #self.get_nuca_response(yr, qr)

    def get_latest_data(self):
        '''Returns the latest date
        '''
        latest_row = Rate.objects.all().order_by('-year').first()


        # will considering the total year will be 0
        if not latest_row:
            return '2014-q1'
        else:
            year = latest_row.year
        
        final_quarter = None
        list_of_quarters = ['q1', 'q2', 'q3', 'q4']
        for quarter_value in list_of_quarters:
            qv = getattr(latest_row, quarter_value)
            #print("Result ->",qv, quater_value)
            if qv == 0:
                breakpoint()
                result = f'{year}-{quarter_value}'
                return result
        result = f'{year}-q4'

        return result
    def get_html_page(self, url):
        if not url.startswith('https://'):
            url = self.best_url + url
        response = requests.get(url)
        html_page = html.fromstring(response.content)
        return html_page

    
    def define_index(self, headers_text):
        '''This helps us to detect the index numer for now we don't need 
        to calculate the index number
        '''
        pass

    
    def parse_table(self, html_page):
        '''This returns the table with its product name and data in the format

        '''
        table_details = []
        get_headers_text = html_page.xpath('//table/thead/tr/th/text()')
        print(get_headers_text)
        list_of_rows = html_page.xpath('//table/tbody/tr')
        for table_row in list_of_rows:
            row_details = {}
            list_of_rows_values = table_row.xpath('./td/text()')
            print("The list that will be scraped is :: ", list_of_rows_values)
            try:
                row_details['product'] = list_of_rows_values[0]
                row_details['credit_union'] = list_of_rows_values[1]
                row_details['bank'] = list_of_rows_values[2]
            except:
                row_details = None
            if row_details:    
                table_details.append(row_details)
        return table_details

