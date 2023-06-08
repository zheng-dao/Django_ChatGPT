from django.core.management.base import BaseCommand, CommandError
from app.models import Domain
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
import os
import json
import random
from app_store_tools import get_android

UPTO = 50
app_platform_map = {
        'android':{
            'base_url':'https://play.google.com',
            'search_url':'https://play.google.com/store/search?q=replace_url&c=apps'
        },
        'ios':{
            'base_url':'https://apps.apple.com',
            #'search_url':'https://www.apple.com/us/search/replace_url?src=globalnav'
            'search_url':'https://itunes.apple.com/search?term=replace_url&entity=software&country=US'
        }
    }
LIST_OF_USER_AGENTS ='''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36
Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36
Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'''

class Command(BaseCommand):
    help = "scrape app url"
    def add_arguments(self, parser):
        parser.add_argument('app_platform', type=str, help="help to define the platform")

    def handle(self, *args, **option):
        co_type = 'credit_union'
        app_platform = option.get('app_platform')
        if not app_platform:
            app_platform = 'android'
        self.app_platform = app_platform
        self.base_url = app_platform_map[app_platform]['base_url']
        self.search_url = app_platform_map[app_platform]['search_url']

        domain_objects = Domain.objects.filter(company__company_type=co_type, company__is_active=True).order_by('-total_assets')[:UPTO]
        details_list = []
        for domain_object in domain_objects:
            self.domain_name = domain_object.name
            print('Working on domain >>>', self.domain_name)
            if self.app_platform == 'android':
                response = self.get_response(self.domain_name)
            elif self.app_platform == 'ios':
                response = self.get_response(domain_object.company.name)
            url_param = self.get_first_url(response)
            if url_param:
                print("Getting the url >>>", url_param)
                details = self.save_page(url_param)
                print("Saved the page")
                details_list.append(details)
                self.save_json(details_list)
    
    def save_json(self, list_file):
        with open(f'{self.root_path}/details_{self.app_platform}.json','w') as out_file:
            json.dump(list_file, out_file, indent=2, ensure_ascii=False)
            
    def get_response(self, search_param):
        '''Returns the response 
        '''
        if app_platform == 'ios':
            search_param = search_param.replace(' ', '+')
        url = self.search_url.replace('replace_url', search_param)
        headers = {'User-Agent': random.choice(LIST_OF_USER_AGENTS.split('\n'))}
        try:
            resp = requests.get(url, headers=headers)
        except Exception as e:
            print("Error while requesting >>", resp)
            resp = None
        return resp

    #https://play.google.com/store/apps/details?id=com.afcu.mobilebanking
    #https://apps.apple.com/us/app/usaa-mobile/id312325565
    def get_first_url(self, response):
        '''Returns the first url of the app store page
        '''
        url_param = None
        if self.app_platform == 'android':
            soup = BeautifulSoup(response.content, 'html.parser')
            regex = re.compile('.*/store/apps/details.*')
            url_param = soup.find_all("a", {"href" : regex})
        elif self.app_platform == 'ios':
            j = json.loads(response.content)
            if len(j['results']) > 0:
                return j['results'][0]['trackViewUrl']
        if url_param:
            return url_param[0]['href']
        return url_param
   
    def save_page(self, url):
        '''Saves page
        '''
        if self.app_platform == 'android' or self.app_platform == 'ios':
            if self.app_platform == 'android':
                url = self.base_url + url
            time.sleep(3)
            response = requests.get(url)
            path_folder = ''
            date_folder = datetime.today().strftime('%Y-%m-%y')
            if not os.path.isdir(path_folder):
                folders = ['reviews', date_folder]
                root_path = 'app/data'
                for folder in folders:
                    root_path = os.path.join(root_path, folder)
                    if not os.path.isdir(root_path):
                        os.mkdir(root_path)
            file_name = f'{url.replace(".","_").replace(":","_").replace("/","_").replace("?","_")}.html'
            self.root_path = root_path
            with open(os.path.join(root_path, file_name), 'wb') as html_file:
                html_file.write(response.content)
            page_details = {
                'file_name':file_name,
                'url'+'_'+self.app_platform:url,
                'domain_name':self.domain_name
            }
            return page_details
                    

