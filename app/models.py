import os
from django.apps import apps
from django.db import models
from django.db.models import Avg, Sum, Max, Min, Count
from django.db.models import Q
from django.contrib.auth.models import User
import json
import re
from datetime import date, datetime, timedelta
from dateutil import parser
from timedate import get_qtr, get_month
import time, pytz
#from sortedm2m.fields import SortedManyToManyField
from django.conf import settings
from django.apps import apps as get_model_app
#from tldextract import extract
from django.forms.models import model_to_dict
# time_zone = timezone(settings.TIME_ZONE)
from operator import and_, or_
from functools import reduce
from file_tools import load_csv_data, load_json
from django.template import Context, Engine
#import re
#from bs4 import BeautifulSoup

STATE_TO_ABBREV = settings.STATE_TO_ABBREV
DEFAULT_CENSUS_YEAR = 2019

GA_TIMEZONES = [
        ('US/Alaska', 'US/Alaska'),
        ('US/Arizona', 'US/Arizona'),
        ('US/Central', 'US/Central'),
        ('US/Eastern', 'US/Eastern'),
        ('US/Hawaii', 'US/Hawaii'),
        ('US/Mountain', 'US/Mountain'),
        ('US/Pacific', 'US/Pacific'),
    ]
GA_TIMEZONES += [(tz, tz) for tz in pytz.country_timezones['US']]

FIRSTTIME_ML_MODEL_MODES = (
    ('ml', 'Default'),
    ('revenue_per_member', 'Revenue Per Member'),
    ('net_income_per_member', 'Net Income Per Member'),
    ('custom_per_member', 'Custom Metric Per Member'),
)
OFFER_TYPES = (
    (None, 'None'),
    ('fi_visitor', 'By Individual User'),
    ('tiered', 'By User Tier'),
)

COMPANY_TYPE = (
    ('bank', 'Bank'),
    ('credit_union', 'Credit Union'),
    ('nonprofit', 'Nonprofit'),
    ('other', 'Other'),
    ('master', 'Master'),
)
class Company(models.Model):
    number = models.CharField(max_length=20, null=True, blank=True)
    code = models.CharField(max_length=10, null=True, blank=True)
    subcode = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    parse = models.CharField(max_length=255, null=True, blank=True)
    aliases = models.CharField(max_length=255, null=True, blank=True)
    alias_google_sheets = models.CharField(max_length=255, null=True, blank=True)
    company_type = models.CharField(max_length=30, null=True, blank=True, choices=COMPANY_TYPE)
    is_active = models.BooleanField(default=True, blank=True)
    is_client = models.BooleanField(default=False, blank=True)
    is_subscriber = models.BooleanField(default=False, blank=True)
    is_prospect = models.BooleanField(default=False, blank=True)
    ga_timezone = models.CharField(max_length=255, null=True, blank=True, choices=GA_TIMEZONES)
    platform_mode = models.CharField(max_length=255, null=True, blank=True)
    top_us_fi = models.BooleanField(default=False, blank=True)
    top_state_fi = models.BooleanField(default=False, blank=True)
    wp_preview_enabled = models.BooleanField(default=False, blank=True)
    js_version = models.CharField(default='2', max_length=10, null=False, blank=True)
    js_scripts_enabled = models.BooleanField(default=False, blank=True)
    scrape_demo_base_url = models.CharField(max_length=100, null=True, blank=True)
    personalization_is_active = models.BooleanField(default=False, blank=True)
    personalize_all_pages = models.BooleanField(default=True, blank=True)
    biz_enabled = models.BooleanField(default=False, blank=True)
    override_personal_categorization = models.BooleanField(default=False, blank=True)
    use_firttime_ml_model = models.BooleanField(default=False, blank=True)
    firttime_ml_model_mode = models.CharField(default='ml', max_length=255, null=True, blank=True, choices=FIRSTTIME_ML_MODEL_MODES)
    use_firsttime_lifetime_value = models.BooleanField(default=False, blank=True)
    custom_personalization_is_active = models.BooleanField(default=False, blank=True)
    general_personalization_is_active = models.BooleanField(default=False, blank=True)
    search_results_page = models.CharField(max_length=255, null=True, blank=True)
    search_query_parameter = models.CharField(max_length=255, null=True, blank=True)
    account_summary_url = models.CharField(max_length=255, null=True, blank=True)
    account_summary_parser = models.CharField(max_length=255, null=True, blank=True)
    use_login_to_infer_member = models.BooleanField(default=False, blank=True)
    trxn_url = models.CharField(max_length=255, null=True, blank=True)
    trxn_parser = models.CharField(max_length=255, null=True, blank=True)
    expiring_balance_to_pmt_ratio = models.FloatField(default=200, null=True, blank=True)
    distressed_percent = models.FloatField(default=300, null=True, blank=True)
    partial_delivery_percent = models.FloatField(default=100, null=True, blank=True)
    always_remember_users_for_partial_delivery = models.BooleanField(default=True, blank=True)
    use_revenue_model = models.BooleanField(default=False, blank=True)
    use_branch_model = models.BooleanField(default=False, blank=True)
    use_rate_model = models.BooleanField(default=False, blank=True)
    offer_type = models.CharField(default=None, max_length=30, null=True, blank=True, choices=OFFER_TYPES)
    company_parent_code = models.CharField(max_length=10, null=True, blank=True)
    cycle_date = models.DateField(null=True, blank=True)
    join_number = models.IntegerField(null=True, blank=True)
    rssd = models.IntegerField(null=True, blank=True)
    cu_type = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    charterstate = models.CharField(max_length=50, null=True, blank=True)
    state_code = models.IntegerField(null=True, blank=True)
    zip_code = models.CharField(max_length=5, null=True, blank=True)
    four_code = models.CharField(max_length=4, null=True, blank=True)
    county_code = models.IntegerField(null=True, blank=True)
    cong_dist = models.IntegerField(null=True, blank=True)
    states_operating_in = models.CharField(max_length=255, null=True, blank=True)
    smsa = models.IntegerField(null=True, blank=True)
    attention_of = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    region = models.IntegerField(null=True, blank=True)
    se = models.CharField(max_length=10, null=True, blank=True)
    district = models.IntegerField(null=True, blank=True)
    year_opened = models.IntegerField(null=True, blank=True)
    tom_code = models.IntegerField(null=True, blank=True)
    limited_inc = models.BooleanField(default=False, blank=True)
    issue_date = models.IntegerField(null=True, blank=True)
    peer_group = models.IntegerField(null=True, blank=True)
    quarter_flag = models.IntegerField(null=True, blank=True)
    timestamp_created = models.DateTimeField(auto_now_add=True, blank=True)
    timestamp_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '%s' % (self.name)

    def get_platform_mode(self, env='stg', return_list=False, next_env=False):
        rval = ''
        if self.platform_mode:
            vals = self.platform_mode.split('|')
            for val in vals:
                if val.startswith(env):
                    if return_list:
                        rval = val.split('=')[1].split(',')
                    else:
                        rval = val.split('=')[1].split(',')[0]
            if not rval and next_env:
                envs = ['local', 'dev', 'stg', 'prod']
                i = envs.index(env)
                for env in envs[i+1:]:
                    if not rval:
                        rval = self.get_platform_mode(env, next_env=True)
        return rval

    def get_scrape_demo_base_dir(self):
        if self.code == 'vys':
            return 'app/static/sites/' + self.code + '/' + 'www.stgfinalyticsdemo.com'
        return 'app/static/sites/' + self.code + '/' + self.scrape_demo_base_url

    def get_subscribers(self, company_type='credit_union', order_by='name'):
        return Company.objects.filter(company_type=company_type, is_subscriber=True, is_active=True).order_by(order_by)

    def get_company_data(self, data_type='personalization'):
        data = {}
        if data_type == 'personalization':
            fields = ['is_subscriber', 'is_client', 'is_active', 'personalization_is_active', 'personalize_all_pages', 'search_results_page', 'search_query_parameter', 'account_summary_url', 'account_summary_parser', 'use_login_to_infer_member', 'trxn_url', 'trxn_parser', 'expiring_balance_to_pmt_ratio', 'distressed_percent', 'partial_delivery_percent', 'always_remember_users_for_partial_delivery', 'use_revenue_model', 'use_branch_model', 'use_rate_model', 'platform_mode']
            for f in fields:
                data[f] = getattr(self, f)
                if f == 'account_summary_parser' and data[f]:
                    data[f] = json.loads(data[f].replace("'", '"'))
        return data

    def remove_models(self, mdls, run_mdl, run_type):
        if run_mdl in mdls and run_type in mdls[run_mdl]:
            mdls[run_mdl].remove(run_type)
        return mdls

    def get_pmodels(self):
        from pmodels import MODEL_TYPES as mdls
        #print(mdls)
        if not self.general_personalization_is_active:
            self.remove_models(mdls, 'ml', 'general')
        if not self.custom_personalization_is_active:
            self.remove_models(mdls, 'ml', 'custom')
        if not self.search_results_page:
            self.remove_models(mdls, 'page', 'search')
        if not self.use_branch_model:
            self.remove_models(mdls, 'geo', 'distance')
        if not self.use_rate_model:
            self.remove_models(mdls, 'rate', 'compare')
            self.remove_models(mdls, 'rate', 'user_data_compare')
        return mdls

    @classmethod
    def get_company(self, code, code_type='code', company_type='credit_union'):
        kwargs = {'company_type':company_type}
        if code_type == 'number':
            kwargs['number'] = code
        else:
            kwargs['code'] = code
        company_instance = self.objects.filter(**kwargs).first()
        return company_instance

    def request_company(self, request, code=None, code_type='number', company_type='credit_union'):
        from account_tools import check_all_staff
        company_instance = None
        user = request.user
        if user.is_authenticated():
            code = request.GET.get('cu_id', code)
            company_type = request.GET.get('company_type', company_type)
            kwargs = {'company_type':company_type}
            if code_type == 'number':
                kwargs['number'] = code
            else:
                kwargs['code'] = code
            if check_all_staff(user):
                company_instance = self.objects.filter(**kwargs).first()
        return company_instance

    @classmethod
    def is_company_client(self, code):
        try:
            company_instance = self.objects.get(code=code, is_client=True)
            return company_instance
        except:
            return None

    def import_data(self, data, analytics_platform_code='ncua'):
        company_type = 'credit_union'
        if analytics_platform_code == 'fdic':
            company_type = 'bank'
        if isinstance(data, list):
            instances = []
            createds = []
            for d in data:
                #print(d)
                d['zip_code'] = d['zip_code'][:5]
                d['street'] = d['street'][:50]
                d['company_type'] = company_type
                c, created = Company.objects.update_or_create(number=d['number'], company_type=d['company_type'], defaults=d)
                instances.append(c)
                createds.append(created)
            return instances, createds
        elif isinstance(data, dict):
            data['zip_code'] = data['zip_code'][:5]
            data['street'] = data['street'][:50]
            data['company_type'] = company_type
            c, created = Company.objects.update_or_create(number=data['number'], company_type=d['company_type'], defaults=data)
            return c, created

    def get_states(self):
        remove_list = ['', None]
        states = Company.objects.values_list('state', flat=True)
        sl = list(set(states))
        [sl.remove(s) for s in remove_list if s in sl]
        return sl

    class Meta:
        ordering = ('is_subscriber', 'name',)
        verbose_name_plural = "companies"

class NonFICompany(models.Model):
    number = models.CharField(max_length=20, null=True, blank=True)
    code = models.CharField(max_length=10, null=True, blank=True)
    subcode = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    parse = models.CharField(max_length=255, null=True, blank=True)
    aliases = models.CharField(max_length=255, null=True, blank=True)
    alias_google_sheets = models.CharField(max_length=255, null=True, blank=True)
    company_type = models.CharField(max_length=30, null=True, blank=True, choices=COMPANY_TYPE)
    is_active = models.BooleanField(default=True, blank=True)
    is_client = models.BooleanField(default=False, blank=True)
    is_subscriber = models.BooleanField(default=False, blank=True)
    is_prospect = models.BooleanField(default=False, blank=True)
    ga_timezone = models.CharField(max_length=255, null=True, blank=True, choices=GA_TIMEZONES)
    platform_mode = models.CharField(max_length=255, null=True, blank=True)
    top_us_fi = models.BooleanField(default=False, blank=True)
    top_state_fi = models.BooleanField(default=False, blank=True)
    scrape_demo_base_url = models.CharField(max_length=100, null=True, blank=True)
    personalization_is_active = models.BooleanField(default=False, blank=True)
    personalize_all_pages = models.BooleanField(default=True, blank=True)
    use_firttime_ml_model = models.BooleanField(default=False, blank=True)
    firttime_ml_model_mode = models.CharField(default='ml', max_length=255, null=True, blank=True, choices=FIRSTTIME_ML_MODEL_MODES)
    use_firsttime_lifetime_value = models.BooleanField(default=False, blank=True)
    custom_personalization_is_active = models.BooleanField(default=False, blank=True)
    general_personalization_is_active = models.BooleanField(default=False, blank=True)
    search_results_page = models.CharField(max_length=255, null=True, blank=True)
    search_query_parameter = models.CharField(max_length=255, null=True, blank=True)
    account_summary_url = models.CharField(max_length=255, null=True, blank=True)
    account_summary_parser = models.CharField(max_length=255, null=True, blank=True)
    trxn_url = models.CharField(max_length=255, null=True, blank=True)
    trxn_parser = models.CharField(max_length=255, null=True, blank=True)
    partial_delivery_percent = models.FloatField(default=100, null=True, blank=True)
    always_remember_users_for_partial_delivery = models.BooleanField(default=True, blank=True)
    use_revenue_model = models.BooleanField(default=False, blank=True)
    use_branch_model = models.BooleanField(default=False, blank=True)
    use_rate_model = models.BooleanField(default=False, blank=True)
    offer_type = models.CharField(default=None, max_length=30, null=True, blank=True, choices=OFFER_TYPES)
    company_parent_code = models.CharField(max_length=10, null=True, blank=True)
    cycle_date = models.DateField(null=True, blank=True)
    join_number = models.IntegerField(null=True, blank=True)
    rssd = models.IntegerField(null=True, blank=True)
    cu_type = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    charterstate = models.CharField(max_length=50, null=True, blank=True)
    state_code = models.IntegerField(null=True, blank=True)
    zip_code = models.CharField(max_length=5, null=True, blank=True)
    four_code = models.CharField(max_length=4, null=True, blank=True)
    county_code = models.IntegerField(null=True, blank=True)
    cong_dist = models.IntegerField(null=True, blank=True)
    smsa = models.IntegerField(null=True, blank=True)
    attention_of = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    region = models.IntegerField(null=True, blank=True)
    se = models.CharField(max_length=10, null=True, blank=True)
    district = models.IntegerField(null=True, blank=True)
    year_opened = models.IntegerField(null=True, blank=True)
    tom_code = models.IntegerField(null=True, blank=True)
    limited_inc = models.BooleanField(default=False, blank=True)
    issue_date = models.IntegerField(null=True, blank=True)
    peer_group = models.IntegerField(null=True, blank=True)
    quarter_flag = models.IntegerField(null=True, blank=True)
    timestamp_created = models.DateTimeField(auto_now_add=True, blank=True)
    timestamp_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name_plural = "Companies: Non-FI"

    def import_nonprofit_csv(fn, fp='app/data/nonprofit'):
        m = {}
        rows = load_csv_data(fn, fp)
        h = rows[0]
        for r in rows[1:]:
            nd = {'company_type':'nonprofit'}
            d = dict(zip(h,r))
            for i,v in m.items():
                if i == 'ZIP':
                    nd[v] = d[i].split('-')[0]
                else:
                    nd[v] = d[i]
            n = NonFICompany(**nd).save()
        print('import of', fn, 'completed')

class Contact(models.Model):
    ccategory = (
        ('prospect', 'Prospect'),
        ('client', 'Client'),
        ('user', 'Finalytics User'),
        ('fi_visitor', 'Client Site Visitor'),
        ('extractable', 'Extractable'),
    )
    csubcategory = (
        ('bank', 'Bank'),
        ('credit_union', 'Credit Union'),
        ('other', 'Other'),
    )
    contact_type = models.CharField(max_length=30, null=True, blank=True)
    category = models.CharField(max_length=30, null=True, blank=True, choices=ccategory)
    subcategory = models.CharField(max_length=30, null=True, blank=True, choices=csubcategory)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    visitor_id = models.CharField(max_length=254, null=True, blank=True)
    id_type = models.CharField(max_length=254, null=True, blank=True)
    offer_tier = models.CharField(max_length=30, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    email_address = models.EmailField(max_length=50, null=True, blank=True)
    email_address2 = models.EmailField(max_length=50, null=True, blank=True)
    email_address3 = models.EmailField(max_length=50, null=True, blank=True)
    phone_default = models.CharField(max_length=50, null=True, blank=True)
    phone_default_type = models.CharField(max_length=50, null=True, blank=True)
    phone_landline = models.CharField(max_length=50, null=True, blank=True)
    phone_work = models.CharField(max_length=50, null=True, blank=True)
    phone_mobile = models.CharField(max_length=50, null=True, blank=True)
    phone_alt1 = models.CharField(max_length=50, null=True, blank=True)
    phone_alt2 = models.CharField(max_length=50, null=True, blank=True)
    fax = models.CharField(max_length=50, null=True, blank=True)
    location_id = models.IntegerField(null=True, blank=True)
    zip_code = models.CharField(max_length=30, null=True, blank=True)
    added_by_uid = models.CharField(max_length=30, null=True, blank=True)
    timestamp_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    timestamp_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ('first_name', 'last_name')
        verbose_name_plural = "contacts"

    def __str__(self):
        return '%s %s %s %s' % (self.first_name, self.last_name, self.phone_default, self.email_address)

    def get_data(self, type='prospect', subtype=None):
        yr = datetime.now().year
        mo = datetime.now().month
        mo_last = mo - 1
        if mo - 1 == 0:
            mo_last = 12
        mo_last_str = str('%02d' % mo_last)
        mo_str = str('%02d' % mo)
        kwargs = {}
        data = None
        yr_str = str(yr)
        last_day = str('%02d' % monthrange(yr, mo)[1])
        date_start = '-'.join((yr_str, '01', '01'))
        date_start_mo_last = '-'.join((yr_str, mo_last_str, '01'))
        date_start_mo = '-'.join((yr_str, mo_str, '01'))
        date_end = '-'.join((yr_str, mo_str, last_day))

        kwargs['timestamp_created__gte'] = date_start
        kwargs['timestamp_created__lte'] = date_end
        kwargs['category'] = type
        if subtype:
            kwargs['subcategory'] = subtype
        data = info.objects.values('id', 'timestamp_created').filter(Q(**kwargs))
        c_age = []
        for contact in data:
            c_age.append(time.mktime(contact['timestamp_created'].timetuple()))
        avg_age = datetime.now() - datetime.utcfromtimestamp(sum(c_age) / len(c_age))
        data_count = data.aggregate(ccount=Count('id'))
        kwargs['timestamp_created__gte'] = date_start_mo
        data_count_mo = data.filter(Q(**kwargs)).aggregate(ccount=Count('id'))
        kwargs['timestamp_created__gte'] = date_start_mo_last
        data_count_mo_last = data.filter(Q(**kwargs)).aggregate(ccount=Count('id'))
        data_dict = {'This Year': data_count['ccount'], 'This Month': data_count_mo['ccount'],
                     'Last Month': data_count_mo_last['ccount'], 'Average Age of Lead': avg_age}
        return data_dict


class Account(models.Model):
    ACCOUNT_TYPES = (
        ('free', 'Free'),
        ('gold', 'Gold'),
        ('master', 'Master'),
        ('platinum', 'platinum'),
    )
    account_type = models.CharField(max_length=50, null=True, blank=True, choices=ACCOUNT_TYPES)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    pmt_customer_id = models.CharField(max_length=50, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    is_subscriber = models.BooleanField(default=False, blank=True)
    paid_status = models.IntegerField(null=True, blank=True)
    pmt_method_expiring = models.BooleanField(default=False, blank=True)
    ts_expiring = models.IntegerField(null=True, blank=True)
    billing_first_name = models.CharField(max_length=50, null=True, blank=True)
    billing_last_name = models.CharField(max_length=50, null=True, blank=True)
    billing_email_address = models.EmailField(max_length=50, null=True, blank=True)
    billing_phone = models.CharField(max_length=50, null=True, blank=True)
    billing_address_line1 = models.CharField(max_length=100, null=True, blank=True)
    billing_address_line2 = models.CharField(max_length=100, null=True, blank=True)
    billing_unit_number = models.CharField(max_length=30, null=True, blank=True)
    billing_city = models.CharField(max_length=50, null=True, blank=True)
    billing_state_abbrev = models.CharField(max_length=2, null=True, blank=True)
    billing_zip_code = models.CharField(max_length=5, null=True, blank=True)
    billing_zip_4code = models.CharField(max_length=4, null=True, blank=True)
    billing_country = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=False, blank=True)
    added_by_uid = models.CharField(max_length=30, null=True, blank=True)
    balance = models.IntegerField(null=True, blank=True)
    date_deactivated = models.DateTimeField(null=True, blank=True)
    date_reactivated = models.DateTimeField(null=True, blank=True)
    deactivated_intentionally = models.BooleanField(default=False, blank=True)
    timestamp_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    timestamp_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "accounts"
        ordering = ('timestamp_modified',)

    def __str__(self):
        if self.company_id:
            returnstr = '%s' % (self.company_id)
        elif self.contact_id:
            returnstr = '%s %s' % (self.contact_id.first_name, self.contact_id.last_name)
        else:
            returnstr = 'None'
        return returnstr

    def get_account(self, account_id=None, owner=None, account_type=None, is_active=None, kws=None):
        if account_id:
            acct = self.objects.get(id=account_id)
            return acct
        else:
            if kws:
                kwargs = kws
            else:
                kwargs = {}
            if owner:
                kwargs['owner'] = owner
            if account_type:
                kwargs['account_type'] = account_type
            if is_active:
                kwargs['is_active'] = is_active
            if kwargs:
                accts = self.objects.filter(**kwargs).order_by('-timestamp_modified')
            else:
                accts = self.objects.all().order_by('-timestamp_modified')
            return accts

    def get_acct_data(self, acct_type='free', acct_subtype=None):
        yr = datetime.now().year
        mo = datetime.now().month
        mo_last = mo - 1
        if mo - 1 == 0:
            mo_last = 12
        mo_last_str = str('%02d' % mo_last)
        mo_str = str('%02d' % mo)
        kwargs = {}
        contact_data = None
        yr_str = str(yr)
        last_day = str('%02d' % monthrange(yr, mo)[1])
        date_start = '-'.join((yr_str, '01', '01'))
        date_start_mo_last = '-'.join((yr_str, mo_last_str, '01'))
        date_start_mo = '-'.join((yr_str, mo_str, '01'))
        date_end = '-'.join((yr_str, mo_str, last_day))

        kwargs['timestamp_created__gte'] = date_start
        kwargs['timestamp_created__lte'] = date_end
        if acct_type == 'free':
            excluded = ['master']
        acct_data = self.objects.values('id', 'timestamp_created').filter(Q(**kwargs)).exclude(
            account_type__in=excluded)
        a_age = []
        for a in acct_data:
            a_age.append(time.mktime(a['timestamp_created'].timetuple()))
        account_avg_age = datetime.now() - datetime.utcfromtimestamp(sum(a_age) / len(a_age))
        acct_data_count = acct_data.aggregate(ccount=Count('id'))
        kwargs['timestamp_created__gte'] = date_start_mo
        acct_data_count_mo = acct_data.filter(Q(**kwargs)).aggregate(ccount=Count('id'))
        kwargs['timestamp_created__gte'] = date_start_mo_last
        acct_data_count_mo_last = acct_data.filter(Q(**kwargs)).aggregate(ccount=Count('id'))
        acct_data_dict = {'This Year': acct_data_count['ccount'], 'This Month': acct_data_count_mo['ccount'],
                          'Last Month': acct_data_count_mo_last['ccount'], 'Account Age': account_avg_age}
        print(kwargs)
        return acct_data_dict


class AccountComment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)


class UserProfile(models.Model):
    # SIGNAL: Check to see if all terms & conditions have been accepted.
    # Extends User model.
    # TBD Some fields like email, username, password can be deleted.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uid = models.CharField(max_length=30, null=True, blank=True)
    password_update_date = models.DateTimeField(null=True, blank=True)
    force_password_reset_date = models.DateTimeField(null=True, blank=True)
    force_password_reset = models.BooleanField(default=False, blank=True)
    mfa_setup_complete = models.BooleanField(default=False, blank=True)
    ip = models.CharField(max_length=255, null=True, blank=True)
    ip_city = models.CharField(max_length=60, null=True, blank=True)
    ip_state = models.CharField(max_length=2, null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    is_client = models.BooleanField(default=False, blank=True)
    is_account_owner = models.BooleanField(default=False, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    #location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    terms_approved = models.BooleanField(default=False, blank=True)
    user_type = models.CharField(max_length=30, null=True, blank=True)
    customer_type = models.CharField(max_length=30, null=True, blank=True)
    user_role = models.CharField(max_length=30, null=True, blank=True)
    user_paid_status = models.IntegerField(null=True, blank=True)
    current_timezone = models.CharField(max_length=30, null=True, blank=True)
    notification_prefs_flag = models.BooleanField(default=False, blank=True)
    email_is_confirmed = models.BooleanField(default=False, blank=True)
    first_password_is_set = models.BooleanField(default=False, blank=True)
    send_test_msgs = models.BooleanField(default=False, blank=True)
    timestamp_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    timestamp_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

class KeywordGroup(models.Model):
    keyword = models.CharField(max_length=150, null=True, blank=True)
    code = models.CharField(max_length=30, null=True, blank=True)
    is_free = models.BooleanField(default=False, blank=True)
    is_core_product = models.BooleanField(default=False, blank=True)
    is_primary_product = models.BooleanField(default=False, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    is_biz = models.BooleanField(default=False, blank=True)
    category = models.CharField(max_length=50, null=True, blank=True)
    subcategory = models.CharField(max_length=50, null=True, blank=True)
    #parent_keyword = models.ForeignKey(ParentKeyword, on_delete=models.SET_NULL, null=True, blank=True, related_name='kg_parent_keyword')
    #rate_type = models.CharField(max_length=10, null=True, blank=True, choices=RATE_TYPES)
    #related_keyword = models.ManyToManyField(Keyword, blank=True)
    total_volume_potential = models.IntegerField(default=False, null=True, blank=True)
    total_clicks = models.FloatField(default=False, null=True, blank=True)
    total_clicks_scaled = models.FloatField(default=False, null=True, blank=True)
    max_total_volume_potential = models.IntegerField(default=False, null=True, blank=True)
    max_total_clicks = models.FloatField(default=False, null=True, blank=True)
    max_total_clicks_scaled = models.FloatField(default=False, null=True, blank=True)
    ppc_total_volume_potential = models.IntegerField(default=False, null=True, blank=True)
    ppc_total_clicks = models.FloatField(default=False, null=True, blank=True)
    ppc_total_clicks_scaled = models.FloatField(default=False, null=True, blank=True)
    ppc_max_total_volume_potential = models.IntegerField(default=False, null=True, blank=True)
    ppc_max_total_clicks = models.FloatField(default=False, null=True, blank=True)
    ppc_max_total_clicks_scaled = models.FloatField(default=False, null=True, blank=True)
    timestamp_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    timestamp_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '%s' % (self.keyword or '')

    def get_product_codes(self, is_core_product=True, is_active=True, flatten_dict=True):
        kg_dict = KeywordGroup.objects.values_list('keyword', 'code').filter(is_core_product=is_core_product, is_active=is_active)
        if flatten_dict:
            return dict(kg_dict)
        return kg_dict

PAGE_TYPES = (
    ('about', 'About'),
    ('blog', 'Blog'),
    ('career', 'Career'),
    ('faq', 'FAQs'),
    ('funnel', 'Funnel'),
    ('home', 'Home'),
    ('login', 'Login/Logout'),
    ('olb', 'OLB'),
    ('offer', 'Offer'),
    ('product', 'Product'),
    ('rate', 'Rate'),
    ('search', 'Search'),
    ('service', 'Service'),
    ('support', 'Support'),
    ('resource', 'Resource'),
    )

PAGE_ATTRIBUTES = {
    'funnel':['funnel'],
    'login':['member'],
    'olb':['member'],
    }

class AdTemplate(models.Model):
    is_active = models.BooleanField(default=False, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    template_name = models.CharField(max_length=255, null=True, blank=True)
    pages = models.TextField(null=True, blank=True)
    ad_method = models.CharField(max_length=50, null=True, blank=True)
    delivery_type = models.CharField(max_length=30, null=True, blank=True)
    div_id = models.CharField(max_length=255, null=True, blank=True)
    div_class = models.CharField(max_length=255, null=True, blank=True)
    div_type = models.CharField(max_length=255, null=True, blank=True)
    ordinal = models.CharField(max_length=20, null=True, blank=True)
    auto_generate = models.BooleanField(default=True, blank=True)
    ad_html = models.TextField(null=True, blank=True)
    headline = models.CharField(max_length=254, null=True, blank=True)
    headline_link = models.TextField(null=True, blank=True)
    subheader = models.CharField(max_length=254, null=True, blank=True)
    subheader_link = models.TextField(null=True, blank=True)
    body_copy = models.CharField(max_length=254, null=True, blank=True)
    link_label = models.CharField(max_length=254, null=True, blank=True)
    link = models.TextField(null=True, blank=True)
    img_link = models.TextField(null=True, blank=True)
    img_width = models.IntegerField(null=True, blank=True)
    custom = models.TextField(null=True, blank=True)
    timestamp_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    timestamp_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.company, self.template_name)

class AdCopy(models.Model):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    is_biz = models.BooleanField(default=False, blank=True)
    keyword_group = models.ForeignKey(KeywordGroup, on_delete=models.SET_NULL, null=True, blank=True)
    content_type = models.CharField(default='product', max_length=255, null=True, blank=True)
    category = models.CharField(default='product', max_length=255, null=True, blank=True)
    subcategory = models.CharField(max_length=255, null=True, blank=True)
    templates = models.CharField(max_length=255, null=True, blank=True)
    headline = models.CharField(max_length=254, null=True, blank=True)
    headline_link = models.TextField(null=True, blank=True)
    subheader = models.CharField(max_length=254, null=True, blank=True)
    subheader_link = models.TextField(null=True, blank=True)
    body_copy = models.CharField(max_length=254, null=True, blank=True)
    link_label = models.CharField(max_length=254, null=True, blank=True)
    link = models.TextField(null=True, blank=True)
    link2_label = models.CharField(max_length=254, null=True, blank=True)
    link2 = models.TextField(null=True, blank=True)
    img_link = models.TextField(null=True, blank=True)
    custom = models.TextField(null=True, blank=True)
    is_dynamic = models.BooleanField(default=False, blank=True)
    timestamp_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    timestamp_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "ad copy"


TIMEFRAME_UNITS = (
    ('days', 'Days'),
    ('hours', 'Hours'),
    ('minutes', 'Minutes'),
    ('seconds', 'Seconds'),
    )
class Ad(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=False, blank=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    cms_id = models.CharField(max_length=255, null=True, blank=True)
    #campaigns = models.ManyToManyField(Campaign, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    override_products_owned = models.BooleanField(default=False, blank=True)
    is_biz = models.BooleanField(default=False, blank=True)
    force_display = models.BooleanField(default=False, blank=True)
    force_display_use_dates = models.BooleanField(default=False, blank=True)
    keyword_group = models.ForeignKey(KeywordGroup, on_delete=models.SET_NULL, null=True, blank=True)
    content_type = models.CharField(default='product', max_length=255, null=True, blank=True)
    category = models.CharField(default='product', max_length=255, null=True, blank=True)
    subcategory = models.CharField(max_length=255, null=True, blank=True)
    pages = models.TextField(null=True, blank=True)
    ad_method = models.CharField(max_length=50, null=True, blank=True)
    delivery_type = models.CharField(max_length=30, null=True, blank=True)
    div_id = models.CharField(max_length=255, null=True, blank=True)
    div_class = models.CharField(max_length=255, null=True, blank=True)
    div_tracking_label = models.CharField(max_length=255, null=True, blank=True)
    outer_html = models.BooleanField(default=False, blank=True)
    ordinal = models.CharField(max_length=20, null=True, blank=True)
    div_type = models.CharField(max_length=255, null=True, blank=True)
    img_to_replace = models.CharField(max_length=255, null=True, blank=True)
    ad_html = models.TextField(null=True, blank=True)
    start_dt = models.DateTimeField(null=True, blank=True)
    end_dt = models.DateTimeField(null=True, blank=True)
    expiration_views = models.IntegerField(null=True, blank=True)
    expiration_timeframe = models.IntegerField(null=True, blank=True)
    expiration_timeframe_units = models.CharField(default='days', max_length=20, null=True, blank=True, choices=TIMEFRAME_UNITS)
    aggressive_expire = models.BooleanField(default=False, blank=True)
    is_dynamic = models.BooleanField(default=False, blank=True)
    ad_template = models.ForeignKey(AdTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    timestamp_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '%s %s %s %s (%s)' % (self.company, self.name, self.keyword_group, self.pages, self.id)

    def get_company_ads(self, co, is_active=True, modes_list=[]):
        kwargs = {'company':co, 'is_active':is_active}
        if 'contentful' in modes_list:
            kwargs['ad_method'] = 'json'
            kwargs['delivery_type'] = 'json'
        ads = Ad.objects.filter(**kwargs)
        return ads

    def get_unique_pages(self, co):
        ads = Ad.objects.filter(company=co, is_active=is_active)

    def get_model_type(self):
        model_type = self.content_type.title()
        if self.content_type == 'faq':
            model_type = 'FAQAnswer'
        return apps.get_model('app', model_type)

    def get_field_mapping(self):
        field_map = {}
        if self.content_type == 'faq':
            if ' }}' in self.ad_html:
                self.ad_html = self.ad_html.replace(' }}', '}}')
            field_map = {'headline':'faqquestion.qtext', 'body_copy':'atext'}
        if field_map:
            for field, model_field in field_map.items():
                self.ad_html = self.ad_html.replace(('.%s}}')%(field), ('.%s}}')%(model_field))
        return self.ad_html

    def create_dynamic_ad_html(self, products_recommended={}, products_owned=[], sorted_products_list=[], id_val=None, id_type=None, geo=None, add_ctas=True, scrape_demo=False, order_by='order'):
        from google_tools import get_ctas
        from pmodels import get_demo_ad_html, merge_products_owned, remove_products_owned
        mdl = self.get_model_type()
        exkwargs = {}
        print('DYNAMIC AD')
        print('pr', products_recommended)
        print('po', products_owned)
        print('sorted', sorted_products_list)
        kwargs = {}
        if self.content_type != 'nonficompany':
            kwargs['company'] = self.company
        if self.content_type == 'content':
            order_by = '-order'
            kwargs['is_active'] = True
            if not id_type:
                id_type = self.category
            if not id_val:
                id_val = self.subcategory
            if id_type:
                kwargs['category'] = id_type
            if id_val:
                kwargs['subcategory'] = id_val
            print(('GEO-content', geo))
            if geo and id_type == 'location' and id_val in geo:
                print('we have a county')
                kwargs['trigger_value'] = geo[id_val]
        elif self.content_type == 'faq':
            qtype_list = ['sales', 'cs']
            if not products_owned:
                qtype_list.remove('cs')
            if products_recommended or products_owned:
                kwargs['faqquestion__keyword_group__keyword__in'] = merge_products_owned(products_recommended, products_owned)

            kwargs['faqquestion__domain__company'] = kwargs.pop('company')
            kwargs['faqquestion__qtype__in'] = qtype_list
            order_by = 'aorder'
        elif self.content_type == 'offer':
            kwargs['visitor_id'] = id_val
            if id_val:
                kwargs['id_type'] = id_type
                if not id_type:
                    kwargs['id_type'] = self.company.offer_type
            #if products_recommended and not sorted_product_list:
            #    sorted_product_list = remove_products_owned(products_recommended, products_owned)
            if products_owned:
                if isinstance(products_owned, list):
                    exkwargs['keyword_group__keyword__in'] = products_owned
                else:
                    exkwargs['keyword_group__keyword'] = products_owned
        elif self.content_type == 'nonficompany':
            print('*************************',geo)
            if geo and geo.get('zipcode'):
                print('*************************',geo)
                kwargs['zip_code'] = geo.get('zipcode')
                order_by = 'id'

        print(kwargs)
        self.ad_html = self.get_field_mapping()
        items = mdl.objects.filter(**kwargs).exclude(**exkwargs).order_by(order_by)
        print(items.count())
        #if self.content_type == 'nonficompany':
        items = items[:5]
        t = Engine().from_string(self.ad_html)
        c = Context({'items':items})
        html = t.render(c)
        if geo:
            if '<fin id="city">' in html and geo and 'city' in geo:
                soup = BeautifulSoup(html, "lxml")
                replaceString =  '<fin id="city">' + geo['city']
                html = str(soup).replace(str(soup.span), replaceString).replace('<html><body>', '').replace('</body></html>', '')
        if add_ctas:
            self.ad_html = html
            html = get_ctas(self.__dict__)['ad_html']
        #html = get_demo_ad_html(ad_template.company, html, scrape_demo)
        return html

    def create_ad_html(self, ad_template='', ad_copy=None, geo=None, add_ctas=True, scrape_demo=False):
        from google_tools import get_ctas
        from pmodels import get_demo_ad_html
        co = self.company
        if not co:
            if isinstance(ad_template, AdTemplate):
                co = ad_template.company
            if not co:
                if isinstance(ad_copy, AdCopy):
                    co = ad_copy.company

        t = Engine().from_string(self.ad_html)
        if isinstance(ad_template, (AdTemplate, Ad,)):
            t = Engine().from_string(ad_template.ad_html)
        c = Context(ad_copy)
        if isinstance(ad_copy, AdCopy):
            c = Context(ad_copy.__dict__)
        html = t.render(c)
        if geo:
            if '<fin id="city">' in html and geo and 'city' in geo:
                soup = BeautifulSoup(html, "lxml")
                replaceString =  '<fin id="city">' + geo['city']
                html = str(soup).replace(str(soup.span), replaceString).replace('<html><body>', '').replace('</body></html>', '')
        if add_ctas:
            self.ad_html = html
            html = get_ctas(self.__dict__)['ad_html']
        html = get_demo_ad_html(co, html, scrape_demo)
        return html

    def ingest_entry(self, entry, data, platform, co=None):
        print('attempting to ingest entry', platform)
        ad = None
        j = entry.copy()
        if isinstance(co, str):
            co = Company.objects.filter(code=co).first()
        if platform == 'contentful':
            print('ingest contentful')
            entry = j['sys']
            fields = j['fields']
            preview = j['finalytics_preview']
            new_item = {
                'cms_id':entry['id'],
                'ad_html':json.dumps(j.fields()),
                'company':co,
                }
            if 'product' in data:
                if 'name' in fields:
                    new_item['name'] = fields.get('name').get('en-US')
                new_item['is_active'] = True
                new_item['keyword_group'] = data['product']
                new_item['category'] = 'product'
                new_item['subcategory'] = 'product'
                new_item['ad_method'] = 'json'
                new_item['delivery_type'] = 'json'
                new_item['div_id'] = entry['contentType']['sys']['id'] + '.content'
            if 'segment' in data:
                new_item['category'] = 'segment'
                new_item['subcategory'] = data['segment']
            ad, created = Ad.objects.update_or_create(cms_id=new_item['cms_id'], defaults=new_item)
            print(ad)
            cdict = {
                'company':co,
                'name':'Test Campaign',
                'code':'test',
                'mode':'test',
                'campaign_type':'standard',
                'delivery_type':'json',
                'is_active':True,
                }
            if 'campaign' in data:
                code = data['campaign']
                cdict['name'] = code
                cdict['code'] = code
            campaign, created = Campaign.objects.get_or_create(company=co, code=cdict['code'], defaults=cdict)
            print(campaign)
            ad.campaigns.add(campaign)
            ad.save()
        return ad


    def set_node(self, path, t_copy, f_value, i=0):
        node = t_copy
        key = path[i]
        print(key, t_copy)
        if i != len(path):
            i += 1
        if i == len(path):
            node[key] = f_value
        else:
            if not key in node:
                print('key is not in node', i)
                if key.isdigit() and key == '0':
                    print('list', path[i-2])
                    node[path[i-2]] = [{}]
                else:
                    node[key] = {}
            if key.isdigit() and key == '0':
                print('a', i, node)
                if isinstance(node[path[i-2]], list):
                    node = node[path[i-2]][0]
            elif path[i] != '0':
                node = node[key]
            print('n', i, node)
            self.set_node(path, node, f_value, i)
        return t_copy

    def save_json_ad_from_template(self, ad_template, ad_copy):
        exclude_field_list = ['id', 'is_active', 'company', 'template_name', 'pages', 'ad_method', 'delivery_type', 'div_id', 'div_class', 'div_type', 'ordinal', 'auto_generate', 'ad_html', 'timestamp_created', 'timestamp_modified']
        fields = ad_template._meta.get_fields()
        t_json = json.loads(ad_template.ad_html)
        t_copy = {}
        for f in fields:
            fname = str(f)
            if fname.startswith('app.'):
                f = fname.split('.')[-1]
                if f not in exclude_field_list:
                    path = (ad_template.div_id + '.' + getattr(ad_template, f)).split('.')
                    f_value = getattr(ad_copy, f)
                    if f_value:
                        t_copy = self.set_node(path, t_copy, f_value)
        return t_copy

    def save_ad_from_template(self, ad_template, ad_copy):
        ad = Ad()
        ad.name = ad_copy.headline
        if not ad_copy.headline:
            ad.name = ad_copy.templates
        ad.is_active = ad_template.is_active
        ad.company = ad_template.company
        if not ad_template.company:
            ad.company = ad_copy.company
        ad.keyword_group = ad_copy.keyword_group
        ad.pages = ad_template.pages
        ad.ad_method = ad_template.ad_method
        ad.delivery_type = ad_template.delivery_type
        ad.div_id = ad_template.div_id
        ad.div_class = ad_template.div_class
        ad.ordinal = ad_template.ordinal
        ad.div_type = ad_template.div_type
        ad.is_dynamic = True
        if ad_template.ad_method == 'json':
            ad.ad_html = json.dumps(self.save_json_ad_from_template(ad_template, ad_copy))
        else:
            ad.ad_html = Ad().create_ad_html(ad_template, ad_copy)
        ad.ad_template = ad_template
        ad.save()
        return ad

    def get_ad_copy_dict(self, remove_fields=['id', 'company_id', '_state', 'pages', 'delivery_type', 'ad_method', 'div_id', 'div_class', 'ordinal', 'div_type', 'img_to_replace', 'outer_html', 'ad_html', 'start_dt', 'end_dt', 'timestamp_created', 'timestamp_modified']):
        d = self.__dict__.copy()
        for rf in remove_fields:
            d.pop(rf, None)
        return d

    def deconstruct_ad_copy(self, fields={'headline':'h1', 'body_copy':'p', 'link':'a'}):
        d = {}
        soup = BeautifulSoup(self.ad_html, 'lxml')
        for k,v in fields.items():
            if k in ['link']:
                elements = soup.findAll(v)
                for i, element in enumerate(elements):
                    if i < 2:
                        tk = k
                        if i > 0:
                            tk = k + str(i+1)
                        d[tk] = element.href
                        d[tk + '_label'] = element.text.strip()
            else:
                element = soup.find(v)
                if element:
                    d[k] = element.text.strip()
        return d

