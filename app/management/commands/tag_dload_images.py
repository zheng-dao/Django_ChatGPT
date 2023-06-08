from django.core.management.base import BaseCommand
import os, sys
from file_tools import traverse_dir, load_json, get_encoding, supermakedirs, save_img_from_url
from django.conf import settings
import chardet
from bs4 import BeautifulSoup
import requests
from app.models import Company, Domain
from google_tools import remove_domain_name

class Command(BaseCommand):
    help = """
    arguments:
        1) -fp: Folder path (required)
        2) -fn: Folder name (required)
        3) -ex: extensions of file
        4) -script: the script which will be replaced
    Example:
        python manage.py tag_src_replace -fp "/static/app/sites/scu/www.schoolsfirstfcu.org" -fn "data-s" -script "data-src" -ex ".html"
    """
    def add_arguments(self, parser):
        parser.add_argument('-fp', nargs='+', type=str, default='app/static/sites')
        parser.add_argument('-fn', type=str)
        parser.add_argument('-ex', nargs='+', type=str, default=['.html'])
        parser.add_argument('-scripts', nargs='+', type=str, default=['div'])
        parser.add_argument('-atts', nargs='+', type=str, default=['style'])
        parser.add_argument('-env', type=str, default='prod')

    def handle(self, *args, **options):
        print(options)
        folder_path = options["fp"]
        folder_name = options["fn"]
        scripts = options["scripts"]
        extensions = options["ex"]
        atts = options["atts"]
        env = options["env"]
        
        co = Company.objects.get(code=folder_name)
        domain = Domain.objects.get(company=co)
        domain_name = domain.name
        if env in ['dev', 'stg']:
            domain_name = co.get_platform_mode(env)

        files = traverse_dir(folder_name, folder_path, extensions=tuple(extensions))

        for file in files:
            print(file)
            error_files = []
            data = None
            default_encoding = 'utf8'
            try:
                with open(file.encode(sys.getfilesystemencoding()), 'r', encoding=default_encoding) as fp:
                    data = fp.read()
            except Exception as e:
                error_files.append(file)
                print(e)

            if data:
                print('getting soup')
                soup = BeautifulSoup(data, 'html.parser')
                print('souped up')
                for script in scripts:
                    elements = soup.find_all(script)
                    for element in elements:
                        for att in atts:
                            last_img = ''
                            if element.has_attr(att):
                                if att == 'style' and 'background-image' in element[att]:
                                    el = element[att]
                                    start = el.find("url('")
                                    end = el.find("')")
                                    last_img = el[start+len("url('"):end].strip().split('?')[0]
                                    if not last_img.startswith('http'):
                                        last_img = 'https://' + domain_name + '/' + last_img
                                elif att != 'style':
                                    last_img = element[att].split(',')[-1].strip().split(' ')[0]
                                    if not last_img.startswith('http'):
                                        last_img = 'https://' + domain_name + '/' + element[att]
                                if last_img:
                                    url_segs = remove_domain_name(last_img)
                                    fn = url_segs[-1]
                                    fpath = (os.sep).join((url_segs[:-1]))
                                    #fp = os.path.join(settings.BASE_DIR, folder_path, folder_name, co.scrape_demo_base_url, fpath).replace('\\', '/')
                                    fp = os.path.join(settings.BASE_DIR, (os.sep).join(folder_path.split('/')), folder_name, co.scrape_demo_base_url, fpath).replace('\\', '/')
                                    #fp = os.path.join(settings.BASE_DIR, folder_path, folder_name, co.scrape_demo_base_url, fpath)
                                    #r = requests.get(last_img)
                                    #encoding = get_encoding(r.text)
                                    try:
                                        username = None
                                        password = None
                                        if co.code == 'cscu':
                                            username = 'cscuprod'
                                            password = '6e2a5a2c'
                                        newpath = save_img_from_url(fn, fp, last_img, username=username, password=password)
                                    except Exception as e:
                                        print(e)
                                        print(fp)
                                    print('------------------')

        if error_files:
            print('These files did not convert.')
            for error in error_files:
                print(error)
            