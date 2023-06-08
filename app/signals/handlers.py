from urllib.request import AbstractBasicAuthHandler
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from allauth.account.signals import email_confirmed, password_set, password_changed, password_reset
from allauth.account.models import EmailAddress
from django.conf import settings
from app.models import Company, UserProfile
#from app.models import Ad, AdCopy, AdTemplate, AppReview, Asset, Campaign, ChartStyle, Company, DataSummary, Domain, GlobalSetting, Keyword, KeywordGroup, Location, Page, State, Tracking, UserProfile
from django.contrib.auth.models import User, Group
from django.db.models import Q, Count, Sum, Max
from datetime import datetime, timedelta, date
import time, timedate
import json
import sys
#from geo_tools import get_lat_long
from allauth.account.signals import *
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
#from geo_tools import get_client_ip,  get_geo_data
#from two_factor.models import PhoneDevice
#from django_otp.plugins.otp_totp.models import TOTPDevice
#from google_tools import strip_special_characters
from django.utils.timezone import make_aware

#from pmodels import PCONFIG, gen_probabilities
from file_tools import save_json

#PCONFIG = cache.get('PCONFIG')

#allauth.account.signals.email_added(request, user, email_address)
@receiver(email_added)
def email_added_(request, user, email_address, **kwargs):
    try:
        ip = get_client_ip(request)
        geo = get_geo_data(ip)
        up = UserProfile.objects.update_or_create(user=user, defaults={'ip':ip, 'ip_city':geo['city'], 'ip_state':geo['state']})
    except Exception as e:
        print(e)

#def asset_presave(sender, **kwargs):
#    instance = kwargs['instance']
#    if instance.url:
#        instance.short_url = instance.url[:255]
#        url_split = instance.url.split('/')
#        instance.filename = url_split[-1]
#        if instance.filename and not instance.name:
#            instance.name = instance.filename.replace('-', '').replace('_', '')

def add_userprofile(instance, **kwargs):
    up = UserProfile.objects.filter(user=instance).first()
    if not up:
        up = UserProfile()
        up.user = instance
        if not up.company:
            if instance.email.endswith(('@finalytics.ai', '@extractable.com')):
                up.company = Company.objects.filter(code='master').first()
            else:
                domain = get_domain_from_email(instance.email)
                if domain:
                    up.company = domain.company
        up.password_update_date = datetime.now()
        up.save()
    
#def calc_rollup(sender, instance, **kwargs):
#    last_field = instance.last_field_updated
#    if instance.base_data_interval != 'quarterly':
#        instance.q1 = sum(filter(None, [instance.m01, instance.m02, instance.m03]))
#        instance.q2 = sum(filter(None, [instance.m04, instance.m05, instance.m06]))
#        instance.q3 = sum(filter(None, [instance.m07, instance.m08, instance.m09]))
#        instance.q4 = sum(filter(None, [instance.m10, instance.m11, instance.m12]))
#    instance.total = sum(filter(None, [instance.q1, instance.q2, instance.q3, instance.q4]))

#def create_code(sender, instance, **kwargs):
#    if isinstance(instance, KeywordGroup):
#        if instance.keyword:
#            instance.code = strip_special_characters(instance.keyword).replace(' ', '').lower()
#    elif isinstance(instance, Campaign):
#        if instance.name:
#            instance.code = strip_special_characters(instance.name).replace(' ', '').lower()

#def get_ga_timezone(sender, instance, **kwargs):
#    if not instance.ga_timezone and instance.state:
#        state = State.objects.filter(state_abbrev=instance.state).first()
#        if state:
#            instance.ga_timezone = state.timezone

def set_user_active(sender, instance, **kwargs):
    user = User.objects.get(email=instance.email)
    user.is_active = True
    user.save()
    up, created = UserProfile.objects.get_or_create(user=user)
    up.email_is_confirmed = True
    up.save()
    
def set_new_user_inactive(sender, instance, **kwargs):
    if instance._state.adding is True:
        print("Creating Inactive User")
        instance.is_active = False
    else:
        print("Updating User Record")

#def print_hi(sender, instance, **kwargs):
#    print('hi')

#def keyword_calcs(instance, **kwargs):
#    instance.finrawExactClicksPerMonth = instance.rawExactClicksPerDay*30
#    instance.finrawPhraseClicksPerMonth = instance.rawPhraseClicksPerDay*30
#    instance.finrawBroadClicksPerMonth = instance.rawBroadClicksPerDay*30
#    instance.finExactClicksPerMonth = instance.rawExactLocalMonthlySearchVolume*instance.rawExactCTR
#    instance.finPhraseClicksPerMonth = instance.rawPhraseLocalMonthlySearchVolume*instance.rawPhraseCTR
#    instance.finBroadClicksPerMonth = instance.rawBroadLocalMonthlySearchVolume*instance.rawBroadCTR
#    instance.clicks = instance.finExactClicksPerMonth
#    instance.ctr = instance.rawExactCTR
#    instance.monthly_volume = instance.rawExactLocalMonthlySearchVolume

#def get_latlong_signal(instance, **kwargs):
#    if not instance.latitude:
#        try:
#            lat, lon = get_lat_long(instance)
#            instance.latitude = lat
#            instance.longitude = lon
#        except Exception as e:
#            print(e, instance)

#def validate_json(instance, **kwargs):
#    json.loads(instance.highcharts_style)
#    print('error in ', instance)

#def get_short_url(instance, **kwargs):
#    instance.url_length = len(instance.url)
#    if instance.url and not instance.short_url:
#        instance.short_url = instance.url[:255]

#def parse_dt(instance, **kwargs):
#    if instance and instance.dt:
#        instance.year = instance.dt.year
#        instance.month = instance.dt.month
#        instance.qtr = timedate.get_qtr(instance.dt.month, return_int=True)

#def auto_gen_ads(sender, instance, **kwargs):
#    print('SIGNAL: check for auto_gen_ads')
#    if instance.auto_generate == True:
#        copies = AdCopy.objects.filter(company=instance.company)
#        if not copies:
#            copies = AdCopy.objects.filter(company=None)
#        for c in copies:
#            ad = Ad().save_ad_from_template(instance, c)

def new_lead_notification(sender, instance, created, **kwargs):
    try:
        if settings.ENV_LIVE and settings.ENV_OS=='linux' and created:
            email_body = instance.email
            send_mail('New Finalytics Lead: ' + str(date.today()), email_body, settings.DEFAULT_FROM_EMAIL, settings.NOTIFICATIONS['new_lead'])
    except Exception as e:
        print(e)

def user_presave(instance, **kwargs):
    if not instance.email and '@' in instance.username:
        instance.email = instance.username
    if instance.email:
        instance.username = instance.email        

def get_domain_from_email(email):
    email_split = email.split('@')
    email_split = email_split[-1]
    domain = Domain.objects.filter(name=email_split).first()
    return domain

def pw_updated(sender, **kwargs):
    up = None
    user = kwargs.get('instance', None)
    if user:
        new_password = user.password
        try:
            up = UserProfile.objects.filter(user=user).first()
            old_user = User.objects.get(pk=user.pk)
            old_password = old_user.password
        except User.DoesNotExist:
            old_password = None
        if new_password != old_password and up:
            up.password_updated_date = datetime.now()
            up.force_password_reset = False
            up.force_password_reset_date = None
            up.save()

#def campaign_presave(sender, **kwargs):
#    instance = kwargs['instance']
#    #if instance and instance.campaigns.all().count() == 0:
#    #    instance.campaigns.add(Campaign().create_initial_campaign(instance))
#    if (instance.ad_html and '{' in instance.ad_html) or (instance.img_to_replace and instance.img_to_replace):
#        instance.is_dynamic = True
#    if instance.company and instance.ad_html:
#        assets = Asset.objects.filter(company=instance.company, is_active=False)
#        for asset in assets:
#            if asset.short_url in instance.ad_html:
#                asset.is_active = True
#                asset.save()

#    kwargs = {
#        'company':instance.company,
#        'pages':instance.pages,
#        }
#    if instance.div_id:
#        kwargs['div_id'] = instance.div_id
#    elif instance.div_class:
#        kwargs['div_class'] = instance.div_class
#    if instance.div_tracking_label:
#        ad = Ad.objects.filter(**kwargs).update(div_tracking_label=instance.div_tracking_label)
#    else:
#        ad = Ad.objects.filter(**kwargs).order_by('-timestamp_modified').exclude(div_tracking_label=None).exclude(div_tracking_label='').exclude(pk=instance.id).first()
#        ad_original = Ad.objects.filter(pk=instance.id).first()
#        if ad and ad_original and ad_original.div_tracking_label != instance.div_tracking_label:
#            pass #new ad intentionally set to None or ''
#        elif ad:
#            instance.div_tracking_label = ad.div_tracking_label

#def set_campaign(instance, **kwargs):
#    if instance and instance.campaigns.all().count() == 0:
#        instance.campaigns.add(Campaign().create_initial_campaign(instance))
#        instance.save()
#    #return instance

def userprofile_personalization(instance, **kwargs):
    if instance.user.email:
        u = instance.user
        company = None
        is_customer = False
        if instance.company:
            company = instance.company
        #else:
        #    domain = get_domain_from_email(instance.user.email)
        #    if domain:
        #        company = domain.company
        if company:
            if company.is_prospect or company.is_subscriber:
                is_customer = True
            if is_customer:
                # if it is first user of the company
                companies_count = UserProfile.objects.filter(company=company).count()
                personalization_group = Group.objects.get(name='personalization_staff')
                if companies_count == 1:
                    personalization_group = Group.objects.get(name='personalization_admin')
                
                u.groups.add(personalization_group)
                u.is_staff = True
                u.save()

#def set_mfa_setup_incomplete(instance, **kwargs):
#    userprofile = UserProfile.objects.get(user=instance.user)
#    if userprofile.mfa_setup_complete:
#        userprofile.mfa_setup_complete = False
#        userprofile.save()

#def update_tracking_signals(instance, **kwargs):
#    tracking = Tracking.objects.filter(campaign_id=instance.id)
#    if tracking:
#        if instance.mode == 'prod' and instance.is_active == True:
#            tracking.update(timestamp_production=make_aware(datetime.now()), days_running=0)
#        elif instance.mode == 'test' or instance.is_active == False:
#            prod_time = tracking.first().timestamp_production
#            if prod_time:
#                days = (make_aware(datetime.now()) - prod_time).days
#                tracking.update(days_running = days)

#def populate_node(conf, temp_dict={}, splits=[]):
#    original_splits = conf.setting_name.split('.')
#    if not splits:
#        splits = original_splits
#    for i,split in enumerate(splits):
#        if i == 0:
#            if split != original_splits[-1]:
#                if not split in temp_dict:
#                    temp_dict[split] = {}
#                temp_dict[split] = populate_node(conf, temp_dict[split], splits[i+1:])
#            else:
#                if conf.setting_type == 'list_item':
#                    if (isinstance(temp_dict, dict) and not temp_dict.get(split)) or not split in temp_dict:
#                        temp_dict[split] = []
#                    temp_dict[split].append(conf.getGS([conf.setting_name], return_value=True))
#                else:
#                    temp_dict[split] = conf.getGS([conf.setting_name], return_value=True)
#    return temp_dict

#def custom_pconfig(keys, configs, pconfig=PCONFIG):
#    for key in keys:
#        print(key)
#        confs = configs.filter(setting_category=key)
#        conf = confs.first()
#        if conf:
#            if not conf.company.code in pconfig:
#                pconfig[conf.company.code] = {}
#            if not conf.setting_category in pconfig[conf.company.code]:
#                pconfig[conf.company.code][conf.setting_category] = {}
#            if key == 'products':
#                prod_audiences = ['default', 'default.priority.firsttime', 'default.priority.nonmember', 'default.priority.member']
#                settings = GlobalSetting().getGS(['products.priority.threshold', 'products.priority.sort_margin'], return_dict=True, co=conf.company)
#                if 'probabilities' not in pconfig[conf.company.code][conf.setting_category]:
#                    pconfig[conf.company.code][conf.setting_category]['probabilities'] = {}
#                for prod_aud in prod_audiences:
#                    prods = confs.filter(setting_name=prod_aud)
#                    product_list = prods.values_list('setting_value', flat=True).order_by('setting_order')
#                    settings_dict = {}
#                    settings_dict['product_list'] = product_list
#                    for setting, d in settings.items():
#                        settings_dict[setting.split('.')[-1]] = d.setting_value
#                    probs = gen_probabilities(**settings_dict)
#                    pconfig[conf.company.code][conf.setting_category]['probabilities'][prod_aud.split('.')[-1]] = probs
#            elif key == 'geo':
#                if not 'zipcodes' in pconfig[conf.company.code]:
#                    pconfig[conf.company.code]['zipcodes'] = {}
#                zipcodes = confs.filter(setting_subcategory='zipcode').order_by('setting_order')
#                for i,sz in enumerate(zipcodes):
#                    sname = sz.setting_name
#                    if sname:
#                        splits = sname.split('.')
#                        zc = splits[0]
#                        data_type = splits[1] + 's'
#                        data_id = splits[-1]
#                        if i == 0:
#                            print(sname, zc, data_id)
#                        pcat = pconfig[conf.company.code]['zipcodes']
#                        if zc not in pcat:
#                            pcat[zc] = {}
#                        if data_type not in pcat[zc]:
#                            pcat[zc][data_type] = {}
#                        pcat[zc][data_type][data_id] = float(sz.setting_value)




#def write_pconfig(instance, **kwargs):
#    from app.views import PCONFIG
#    if instance.add_to_pconfig and instance.company:
#        global PCONFIG
#        data = {}
#        if instance.company:
#            code = instance.company.code
#            if code in PCONFIG:
#                data = PCONFIG[code]
#            configs = GlobalSetting.objects.filter(company=instance.company, add_to_pconfig=True)
#            keys = configs.values_list('setting_category', flat=True).distinct()
#            if keys and not instance.company.code in PCONFIG:
#                PCONFIG[instance.company.code] = {}
#            for key in keys:
#                if not key in data:
#                    data[key] = {}

#                #confs = configs.filter(setting_category=key)
#                #for conf in confs:
#                #    if '.' in conf.setting_name:
#                #        temp_dict = populate_node(conf)
#                #        data[key].update(temp_dict.copy())
#                #    else:
#                #        if conf.setting_type == 'list_item':
#                #            if (isinstance(data, dict) and not data.get(key)):
#                #                data[key] = {}
#                #            if conf.setting_name not in data[key]:
#                #                data[key][conf.setting_name] = []
#                #            data[key][conf.setting_name].append(conf.getGS([conf.setting_name], return_value=True))
#                #        else:
#                #            data[key][conf.setting_name] = conf.getGS([conf.setting_name], return_value=True)

#            custom_pconfig(['products', 'geo'], configs, PCONFIG)
#            cache.set('PCONFIG', PCONFIG)
#            try:
#                #print(PCONFIG[code]['products']['probabilities']['default'], 'signals')
#                save_json(PCONFIG[code], 'pconfig.json', fp=('/').join(['app/model_files', code, settings.ENV]), indent=4)
#            except Exception as e:
#                email_body = str(e)
#                send_mail('pconfig did not save for ' + code + ': ' + str(date.today()), email_body, settings.DEFAULT_FROM_EMAIL, settings.NOTIFICATIONS['admins'])


##pre_save.connect(validate_json, sender=ChartStyle)
#pre_save.connect(campaign_presave, sender=Ad)
#pre_save.connect(parse_dt, sender=AppReview)
#pre_save.connect(asset_presave, sender=Asset)
#pre_save.connect(get_ga_timezone, sender=Company)
#pre_save.connect(calc_rollup, sender=DataSummary)
##pre_save.connect(print_hi, sender=EmailAddress)
##pre_save.connect(set_user_active, sender=EmailAddress)
#pre_save.connect(keyword_calcs, sender=Keyword)
#pre_save.connect(create_code, sender=[KeywordGroup, Campaign])
#pre_save.connect(get_latlong_signal, sender=Location)
#pre_save.connect(get_short_url, sender=Page)
pre_save.connect(user_presave, sender=User)
pre_save.connect(pw_updated, sender=User)

##post_save.connect(auto_gen_ads, sender=AdTemplate)
post_save.connect(new_lead_notification, sender=User)
post_save.connect(add_userprofile, sender=User)
#post_save.connect(set_campaign, sender=Ad)
##post_save.connect(set_pw_date, sender=User) #This is handled by a decorator because it applies to 3 different signals from django allauth
#post_save.connect(userprofile_personalization, sender=UserProfile)
#post_save.connect(write_pconfig, sender=GlobalSetting)

#post_delete.connect(set_mfa_setup_incomplete, sender=TOTPDevice)
#post_delete.connect(set_mfa_setup_incomplete, sender=PhoneDevice)
#post_save.connect(update_tracking_signals, sender=Campaign)