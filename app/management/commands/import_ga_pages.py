from django.core.management.base import BaseCommand
from app.models import Company, Domain, Page
import json
from google_tools import predict_url_category, get_domain, remove_domain_name
from file_tools import load_csv_data, save_csv
from django.forms.models import model_to_dict

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-co', type=str)
        parser.add_argument('-cats', type=bool, default=True)

    def handle(self, *args, **options):
        print(options)
        co = Company.objects.get(code=options['co'])
        domain_name = Domain.objects.filter(company=co).first()
        domain_names = [domain_name]
        if domain_name.name.startswith('www.'):
            domain_names.append(domain_name.name.replace('www.', '', 1))
        else:
            domain_names.append('www.'+domain_name.name)

        pages = Page.objects.filter(domain__company=co)
        page_list = pages.values_list('url', flat=True)

        fn = co.code + '_page_view_data.csv'
        fp = 'app/static/sites/' + co.code + '/hts-cache'

        rows = load_csv_data(fn, fp)
        new_rows = [rows[0]]
        print(len(rows))
        url_list = []

        for i, row in enumerate(rows):
            if i != 0:
                url = 'https://' + row[0]
                print(url)
                domain = get_domain(url, instance=False, return_subdomain=True)
                url_path = remove_domain_name(url, return_splits=False, remove_query_params=True)
                if not url_path.startswith('/'):
                    url_path = '/' + url_path
                if options['cats']:
                    category = predict_url_category(url_path)
                    if category:
                        print(category['guessed_category'])
                        print(category)
                        print('')
                        new_rows.append(row + [category['guessed_category'], category['guessed_subcategory']])
                        category['category'] = category.pop('guessed_category', None)
                        category['subcategory'] = category.pop('guessed_subcategory', None)
                    else:
                        new_rows.append(row + ['', ''])
                if url_path and domain in domain_names:
                    pvs = int(row[1].replace(',', ''))
                    if url_path in page_list:
                        pg_index = page_list.index(url_path)
                        pg = pages[pg_index]
                        if url_path in url_list:
                            pg.ga_pageviews = pvs
                        else:
                            url_list.append(url_path)
                            pg.ga_pageviews += pvs
                            pg.save()
                        if category and not pg.is_reviewed:
                            pg.is_categorized = True
                            pg_dict = model_to_dict(pg)
                            pg_dict = dict(pg_dict, **category)
                            Page(**pg_dict).save()
                    else:
                        if url_path in url_list:
                            pg = Page.objects.get(domain=domain_name, short_url=url_path[:255])
                            pg.ga_pageviews += pvs
                            pg.save()
                        else:
                            pg_dict = {
                                'domain':domain_name,
                                'url':url_path,
                                'short_url':url_path[:255],
                                'ga_pageviews':pvs,
                                }
                            if category:
                                pg_dict['is_categorized'] = True
                                pg_dict = dict(pg_dict, **category)
                            Page(**pg_dict).save()
                            url_list.append(url_path)


        url_list = list(set(url_list))
        print(len(url_list))

        for url in url_list:
            print(url)
            #url = 'https://' + url
            #domain = get_domain(url, instance=False, return_subdomain=True)
            #url_path = remove_domain_name(url, return_splits=False)
            #print(url)
            print(domain)

            if options['cats']:
                category = predict_url_category(url)
                if category:
                    print(category['guessed_category'])
                    print(category)
                    print('')
                    #r = input("next?")


        save_csv(new_rows, rows[0] + ['cat', 'subcat'], 'temp_' + fn, fp)