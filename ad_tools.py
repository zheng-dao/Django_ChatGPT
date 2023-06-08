import os
from xml.etree.ElementInclude import include
from app.models import Ad, AdCopy, AdTemplate, Asset, Campaign, Company, Domain, KeywordGroup, Page
from bs4 import BeautifulSoup
from file_tools import get_image_count, get_image_dict, get_image_item, traverse_dir
from google_tools import predict_url_category

def get_base_url(domain, env='prod', is_demo=True):
    base_url = 'https://' + domain.name
    platform_mode = domain.company.get_platform_mode(env)
    if platform_mode:
        base_url = 'https://' + platform_mode
    if env == 'local':
        base_url = 'http://127.0.0.1:8000'
        if not is_demo:
            base_url = 'http://127.0.0.1:8001'
    return base_url

def create_ad_from_template(template, company=None):
    copies = AdCopy.objects.filter(company=company)
    if not company:
        copies = AdCopy.objects.filter(company=None)
    for c in copies:
        ad = Ad().save_ad_from_template(template, c)

def append_to_str_list(s, to_append, delimiter=','):
    final_s = to_append
    if s and to_append:
        if not to_append in s.split(delimiter):
            final_s = s + delimiter + str(to_append)
    return final_s

def find_most_likely_url_by_category(domain, category, order_by='id', funnel_start=False):
    kg = KeywordGroup.objects.filter(keyword=category).first()
    kwargs = {}
    kwargs['domain'] = domain
    kwargs['keyword_group'] = kg
    if funnel_start:
        kwargs['attributes__icontains'] = 'funnel'
    page = Page.objects.filter(**kwargs).order_by(order_by).first()
    return page

def strip_soup(soup, text=['<html><body>', '</body></html>']):
    newsoup = str(soup)
    for t in text:
        newsoup = newsoup.replace(t, '')
    return newsoup

def assign_page_url_to_add_ctas(domain, ad, tag='a'):
    page_funnel = None
    if ad.keyword_group:
        page = find_most_likely_url_by_category(domain, ad.keyword_group.keyword)
        if page:
            soup = BeautifulSoup(ad.ad_html, 'lxml')
            hrefs = soup.findAll(tag)
            for h in hrefs:
                if any(word in h.text.lower() for word in ['open', 'apply', 'join']):
                    page_funnel = find_most_likely_url_by_category(domain, ad.keyword_group.keyword, funnel_start=True)
                    if page_funnel:
                        h['href'] = page_funnel.short_url
                else:
                    h['href'] = page.short_url
            ad.ad_html = strip_soup(soup)
    return ad

def create_generic_ad_copy(ads, fields={'headline':'h1', 'body_copy':'p', 'link':'a'}):
    for h in ads:
        d = h.deconstruct_ad_copy(fields=fields)
        print(d)
        i = h.get_ad_copy_dict()
        print(i.update(d))
        print('--------------------')
        ad = AdCopy(**i).save()
    return ad

def get_all_img_data(co, saveit=False):
    domain = Domain.objects.filter(company=co).first()
    base_dir = co.get_scrape_demo_base_dir()
    files = traverse_dir('', base_dir, ['.html'])
    ifiles = traverse_dir('', base_dir, normalize=False)
    cnt = get_image_count(files)
    id = get_image_dict(ifiles, key='path')

    for k, dimensions in id.items():
        if k in cnt:
            cnt[k].update(dimensions)
        else:
            cnt[k] = dimensions
            cnt[k]['company'] = co
            cnt[k]['domain'] = domain
            cnt[k]['url'] = k
            cnt[k]['short_url'] = k[:254]
            categories = predict_url_category(k)
            cnt[k]['category'] = categories.get('guessed_category')
            cnt[k]['subcategory'] = categories.get('guessed_subcategory')

    if saveit:
        for k, d in cnt.items():
            asset = Asset.objects.filter(domain=domain, short_url=k).first()
            if asset:
                for f in asset._meta.get_fields():
                    value = getattr(asset, f.name)
                    if f.name == 'pages' and value:
                        value = asset.pages + ',' + value
                        setattr(asset, 'pages', value)
                    elif not value:
                        setattr(asset, f.name, value)
            else:
                d.pop('page', None)
                d['company'] = co
                d['domain'] = domain
                d['filename'] = k.split('?')[0].split('/')[-1]
                d['url'] = k
                d['short_url'] = k[:254]
                kg = None
                if d.get('page_category'):
                    kg = KeywordGroup.objects.filter(keyword=d['page_category']).first()
                elif d.get('category'):
                    kg = KeywordGroup.objects.filter(keyword=d['category']).first()
                if kg:
                    d['keyword_group'] = kg
                asset = Asset(**d).save()
    return cnt

def replace_ad_img(domain, ad, tag='img', order_by='id', include_domain_path=False):
    co = domain.company
    base_dir = co.get_scrape_demo_base_dir()
    soup = BeautifulSoup(ad.ad_html, 'lxml')
    kwargs = {
        'domain':domain,
        'keyword_group':ad.keyword_group,
        }
    if ad.ad_template and ad.ad_template.img_width:
        kwargs['width'] = ad.ad_template.img_width
    #print('kwargs')
    #print(ad.ad_template.img_width)
    #print(kwargs)
    if '<img' in ad.ad_html:
        img = soup.find(tag)
        if img:
            asset = Asset.objects.filter(**kwargs).order_by('id').first()
            if asset:
                #width, height = get_image_item(os.path.join(base_dir, asset.short_url))
                img['src'] = asset.short_url
                if include_domain_path and not asset.short_url.startswith('http'):
                    img['src'] = 'https://www.' + domain.name + asset.short_url
        ad.ad_html = strip_soup(soup)
    elif 'background-image:' in ad.ad_html:
        starti = ad.ad_html.index('background-image:')
        endi = ad.ad_html[starti+1:].index(')')
        #quote_type = "'"
        #if ad.ad_html[endi - 1] != quote_type:
        #    quote_type = '"'
        #img = soup.find('div')
        #if img:
        if starti and endi:
            asset = Asset.objects.filter(**kwargs).order_by('id').first()
            if asset:
                img_src = asset.short_url
                if include_domain_path and not asset.short_url.startswith('http'):
                    img_src = 'https://www.' + domain.name + asset.short_url
                rep = ("background-image: url('%s')")%(img_src)
                #width, height = get_image_item(os.path.join(base_dir, asset.short_url))
                #img['style'] = img['style'].replace("background-image: url('');", "background-image: url('" + asset.short_url + "');")
                ad.ad_html = ad.ad_html[:starti] + rep + ad.ad_html[starti + endi + 2:]
    return ad

def gen_demo_pages(co, page_types=['apply', 'open', 'thankyou', 'search']):
    open = ['checking account', 'savings account', 'ira', 'money market account', 'hsa']
    core_products = KeywordGroup.objects.filter(is_core_product=True)
    domain = Domain.objects.filter(company=co).first()
    for pg in page_types:
        print(pg.upper())
        if pg not in ['search']:
            for cp in core_products:
                print(cp.keyword)
                data = {
                    'domain':domain,
                    'demo_only': True,
                }
                data['url'] = '/' + '/'.join((pg, 'static', 'sites', co.code, co.scrape_demo_base_url, cp.keyword))
                data['url_type'] = 'funnel'
                data['category'] = cp.keyword
                data['keyword_group'] = cp
                if pg in ['open', 'apply']:
                    data['is_app_start'] = True
                    data['attributes'] = 'funnel'
                elif pg == 'thankyou':
                    data['is_app_complete'] = True
                    data['attributes'] = 'funnel_end'
                Page(**data).save()
        elif pg == 'search':
            data = {
                'domain':domain,
                'demo_only': True,
            }
            data['url'] = '/results'
            data['url_type'] = 'search'
            data['category'] = 'search'
            data['subcategory'] = 'search results'
            Page(**data).save()


def gen_demo_ads(co, generic_ad_copy=True, gen_img_data=False, img_tag='img', cta_tag='a', template_name=None, include_domain_path=False):
    ad = None
    domain = co
    if not isinstance(domain, Domain):
        domain = Domain.objects.filter(company=co).first()
    templates = AdTemplate.objects.filter(company=co)
    if not generic_ad_copy:
        templates = AdTemplate.objects.filter(company=None)
    adcopy = AdCopy.objects.filter(company=None)
    if not generic_ad_copy:
        adcopy = AdCopy.objects.filter(company=co)
    if template_name:
        templates = templates.filter(template_name=template_name)
        adcopy = adcopy.filter(templates__icontains=template_name)
    if gen_img_data:
        cnt = get_all_img_data(domain.company, gen_img_data)
    print(templates.count, 'templates')
    print(adcopy.count, 'ad copy items')
    for t in templates:
        for adc in adcopy:
            ad = Ad().save_ad_from_template(t, adc)
            print(ad)
            ad = assign_page_url_to_add_ctas(domain, ad, tag=cta_tag)
            ad = replace_ad_img(domain, ad, tag=img_tag, include_domain_path=include_domain_path)
            ad.save()
    if ad:
        return ad
    else:
        print('no ads were created')

