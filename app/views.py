from app.models import Company
#from pyexpat import model
#from signal import signal
#from statistics import mode
#from urllib.request import AbstractBasicAuthHandler
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
import logging
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect, HttpResponse
from allauth.exceptions import ImmediateHttpResponse
from django.forms.models import model_to_dict
from allauth.account.auth_backends import AuthenticationBackend
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

#from django_otp.decorators import otp_required
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, AllowAny, IsAuthenticated, DjangoModelPermissions
#from app.permissions import SafelistPermission
from rest_framework.views import APIView
from rest_framework import status
import json, os, sys, base64
##from OAuth2.OAuth2 import OAuth2
##from OAuth2.ClientCredentials import ClientCredentials
##from OAuth2.Api import Api
from app.models import Company, User, UserProfile
#from app.models import Account, Ad, AdCopy, AdTemplate, AnalyticsPlatform, Asset, Campaign, Chart, ChartStyle, ChartType, Company, Contact, County, DataSummary, Demographic, Domain, FinancialSummary, FAQQuestion, FAQAnswer, FinancialTransaction, FinancialTransactionTest, GlobalSetting, KeywordGroup, Keyword, Location, Log, MultiReport, Notification, NotificationType, Metric, Page, ParentKeyword, Rate, Report, RevenueKPI, Sheet, State, Subscription, SubscriptionPlan, TestScenario, Tier, Tracking, UserProfile, Version, WebAccount, WebProperty, WebToken, ZipCode, Offer
#from app.models import AD_METHOD, DELIVERY_TYPES
#from app.serializers import AccountSerializer, AdSerializer, AnalyticsPlatformSerializer, CampaignSerializer, ChartSerializer, ChartStyleSerializer, ChartTypeSerializer, CompanySerializer, ContactSerializer, DataSummarySerializer, DomainSerializer, GlobalSettingSerializer, FAQQuestionSerializer, FAQAnswerSerializer, KeywordGroupSerializer, LocationSerializer, MultiReportSerializer, NotificationSerializer, MetricSerializer, PageSerializer, ParentKeywordSerializer, ReportSerializer, RevenueKPISerializer, SheetSerializer, SubscriptionSerializer, SubscriptionPlanSerializer, TestScenarioSerializer, TierSerializer, UserSerializer, UserProfileSerializer
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django.conf import settings
from datetime import date, datetime, timedelta
import time
from ga.settings import BASE_DIR; import timedate
from django.utils import timezone
from django.utils.decorators import method_decorator

import pytz

#from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
#from rest_framework.response import Response
#from rest_framework import permissions
#from django.db.models import Count, Prefetch, Q
#from django.utils.decorators import method_decorator

#from django.views import View
#from django.views.decorators.cache import cache_page
#from django.core.cache import cache, caches
#from django.utils import timezone
#from django.core.cache.backends.dummy import DummyCache
#from . import chart_utils , chart_builder
#from geo_tools import get_geo_data, get_client_ip, visitor_ip_address
#from google_tools import predict_url_category
#from secure_tools import get_random_password
#from file_tools import traverse_dir, get_image_dict, get_dir, glob_files, save_json, load_file, path_exists
from account_tools import is_fin_staff, check_all_staff
##from django_otp.decorators import otp_required
#from ad_tools import append_to_str_list, get_base_url

#from apiclient.discovery import build
#import google.oauth2.credentials
#import google_auth_oauthlib.flow
#import googleapiclient.discovery
#from google_tools import CLIENT_SECRETS_FILE, OAUTH_SCOPES
#import requests
#import httplib2
#from bs4 import BeautifulSoup
#from copy import deepcopy

#from two_factor.models import get_available_phone_methods
#from two_factor.views import SetupCompleteView
#from two_factor.models import PhoneDevice
#from django_otp.plugins.otp_totp.models import TOTPDevice
#from .decorators import check_cu_user, check_perms, check_perms_fi, check_cu_user_revised, check_mfa_setup

#import subprocess as sp
#import pandas as pd
#import math
#from scipy.stats import norm
import re
from django.urls import reverse
logging.config.dictConfig(settings.LOGGING)
lg = logging.getLogger(__name__)

#from validate_tools import validate_getads_post

admin_login_url = '/admin'
consumer_login_target_url = '/account/login/'
no_access_url = '/no-access/'

#from file_tools import load_json
#PCONFIG = {'global':{}}
##for code in CO_CODES:
##try:
##    code = 'vys'
##    folder = settings.ENV
##    base_folder = 'app/model_files'
##    fp = os.path.join(base_folder, code, folder)
##    if os.path.exists(fp):
##        j = load_json('pconfig.json', fp=fp)
##        if j:
##            PCONFIG[code] = j
##    else:
##        print('pconfig path does not exist for ', code)
##        #lg.info(('pconfig path does not exist for ', code))
##    try:
##        fp = os.path.join(settings.BASE_DIR, base_folder)
##        top_us = load_json('top_100_fi.json', fp=fp)
##        top_fis = {'us':top_us}
##        top_states = load_json('top_50_state_fi.json', fp=fp)
##        top_fis = dict(top_fis, **top_states)
##        PCONFIG['global']['top_fi'] = top_fis

##        makes = load_json('makes.json', fp=fp)
##        PCONFIG['global']['make'] = makes
##    except Exception as e:
##        print('There was an error importing pconfig.json for the top FI and VehicelMake data json files')
##        print(str(e))
##except Exception as e:
##    print('There was an error importing pconfig.json for ', code)
##    print(str(e))
##    #lg.info(('There was an error importing pconfig.json for ', code))
##    #lg.info(str(e))
#cache.set('PCONFIG', PCONFIG)
##p = cache.get('PCONFIG')
##print(p['vys']['products']['probabilities']['default'], 'views')


## def check_perms(user):
##     allow = False
##     if user.is_superuser or user.is_staff:
##         allow = True
##     return allow

@api_view()
def null_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view()
#@permission_classes((permissions.AllowAny,))
def complete_view(request):
    return Response("Email account is activated")


#@api_view(['GET'])
#@permission_classes([])
#def combine_charts_api(request):
#    kwargs = chart_utils.parse_request_kwargs(request.query_params)
#    chart_data = chart_utils.combine_charts(**kwargs)
#    return Response({'chart_data': chart_data})

#def is_mfa_setup_invalid(user=None):
#    invalid = True
#    if user:
#        phonedevice = PhoneDevice.objects.filter(user=user).exists()
#        totpdevice = TOTPDevice.objects.filter(user=user).exists()
#        if user.userprofile.mfa_setup_complete and (phonedevice or totpdevice):
#            invalid = False
#    return invalid

def is_finalytics_employee(user, current_user_groups=None):
    is_fin_employee = False
    if user.is_superuser:
        is_fin_employee = True
    else:
        if not current_user_groups:
            current_user_groups = user.groups.values_list('name', flat=True)
        # ['finalytics_INTERNAL_personalization_admin', 'finalytics_INTERNAL_personalization_staff']
        # if any(['personalization_admin', 'personalization_staff']) in current_user_groups:
        # if 'personalization_admin' in current_user_groups or 'personalization_staff' in current_user_groups:
        if 'finalytics_INTERNAL_personalization_admin' in current_user_groups or 'finalytics_INTERNAL_personalization_staff' in current_user_groups:
            is_fin_employee = True
    return is_fin_employee

def check_company(request, context):
    user = request.user
    co = user.userprofile.company
    cu_id = co.code
    current_user_groups = user.groups.values_list('name', flat=True)
    is_fin_employee = is_finalytics_employee(user, current_user_groups)
    if is_fin_employee:
        cu_id = request.GET.get('cu_id', None)
        if not cu_id:
            cu_id = request.session.get('cu_id', None)
        if cu_id and cu_id != 'all':
            code_type = 'code'
            if cu_id.isdigit():
                code_type = 'number'
            co = Company().get_company(cu_id, code_type)
            request.session['cu_id'] = cu_id
        elif cu_id == 'all' or cu_id == '':
            request.session['cu_id'] = ''
            context['redirect_url'] = request.path
            context['companies'] = Company.objects.filter(is_subscriber=True)
            context['template'] = 'admin/choose-company.html'
        else:
            context['redirect_url'] = request.path
            context['companies'] = Company.objects.filter(is_subscriber=True)
            context['template'] = 'admin/choose-company.html'

    
    context['company'] = co
    context['cu_id'] = cu_id
    context['user_groups'] = current_user_groups
    context['is_fin_employee'] = is_fin_employee
    return co, current_user_groups, context


## @login_required(login_url=admin_login_url)
#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    template = 'app/index.html'
    context = {}
    #co, ugs, context = check_company(request, context)
    user = request.user
    #up = UserProfile.objects.get(user=user)
    context['subscribers'] = Company.objects.filter(is_subscriber=True)
 
    #if up.force_password_reset:
    #    return HttpResponseRedirect('/accounts/password/change/')
    if not is_finalytics_employee(user):
        #print('hey here', user.email[14:])
        return HttpResponseRedirect('/dashboard')
    #print(request.COOKIES)
    context['title'] = 'Home Page'
    context['site_ip'] = settings.EXTERNAL_SITE_IP
    return render(
        request,
        template,
        context
    )

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms, login_url=no_access_url)
#@check_mfa_setup
#def choose_company(request):
#    """Renders the home page."""
#    assert isinstance(request, HttpRequest)
#    context = {}
#    template = 'admin/choose-company.html'
#    redirect_url = request.path
#    # co, ugs, context = check_company(request, context)
#    user = request.user
#    up = UserProfile.objects.get(user=user)
#    # context['http_referer'] = request.META.get('HTTP_REFERER').split('=')[1]
#    # context['http_referer'] = None
    
#    if 'redirect_url' in request.session:
#        redirect_url = request.session['redirect_url']
#        del request.session['redirect_url']
#    context['redirect_url'] = redirect_url
#    context['companies'] = Company.objects.filter(is_subscriber=True)
#    return render(
#        request,
#        template,
#        context
#    )

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
def dashboard(request):
    template = 'admin/dashboard.html'
    context = {}
    #co, ugs, context = check_company(request, context)
    return render(
        request,
        template,
        context
    )

## @login_required(login_url=admin_login_url)
#def no_access(request):
#    """Renders the home page."""
#    assert isinstance(request, HttpRequest)
#    #print(request.COOKIES)
#    return render(
#        request,
#        'app/no_access.html',
#        {
#            'title': 'No Site Access',
#            'site_ip': settings.EXTERNAL_SITE_IP

#        }
#    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Contact',
            'message': 'Your contact page.',
            'year': datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'About',
            'message': 'Your application description page.',
            'year': datetime.now().year,
        }
    )


#def dynamic_cache():
#    # now = timezone.now()
#    # midnight = (timezone.now()+timedelta(days=1)).replace(hour=0,minute=0,second=0,microsecond=0)
#    # seconds = (midnight-now).seconds
    
#    cache_config =caches['default']
#    if isinstance(cache_config, DummyCache):
#        return cache_page(0)
#    #Cache 12 hours
#    return cache_page(60*60*12)

#class CacheModelViewSet(viewsets.ModelViewSet):
#    @method_decorator(dynamic_cache())
#    def dispatch(self, request, *args, **kwargs):
#        return super().dispatch(request, *args, **kwargs)

#class MyModelPermissions(DjangoModelPermissions):
#    perms_map = {
#        'GET':['%(app_label)s.view_%(model_name)s'],
#        'OPTIONS': [],
#        'HEAD': [],
#        'POST': ['%(app_label)s.add_%(model_name)s'],
#        'PUT': ['%(app_label)s.change_%(model_name)s'],
#        'PATCH': ['%(app_label)s.change_%(model_name)s'],
#        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
#    }

#class PostOnlyModelPermissions(DjangoModelPermissions):
#    perms_map = {
#        'POST': ['%(app_label)s.add_%(model_name)s'],
#    }

#class GetOnlyModelPermissions(DjangoModelPermissions):
#    perms_map = {
#        'GET': ['%(app_label)s.add_%(model_name)s'],
#    }

#class UserViewSet(viewsets.ModelViewSet):
#    permission_classes = [PostOnlyModelPermissions]
#    queryset = User.objects.all()
#    serializer_class = UserSerializer
#    filter_fields = ('id', 'username', 'email', 'is_staff')

#class UserProfileViewSet(viewsets.ModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = UserProfile.objects.all()
#    serializer_class = UserProfileSerializer
#    filter_backends = [DjangoFilterBackend]
#    filter_fields = ('id', 'user__id', 'user__email')

#class Isstaff(permissions.BasePermission):
#    def has_permission(self, request, view):
#        if request.user and request.user.groups.filter(name='staff'):
#            return True
#        return False

#class IsSuperUser(permissions.BasePermission):
#    def has_permission(self, request, view):
#        if request.user and request.user.is_superuser:
#            return True
#        return False

#class AccountViewSet(viewsets.ModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    permission_classes = [MyModelPermissions]
#    queryset = Account.objects.all()
#    serializer_class = AccountSerializer

##@permission_classes([Isstaff|IsSuperUser])
#class AdViewSet(viewsets.ModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = Ad.objects.all()
#    serializer_class = AdSerializer
#    filter_backends = [DjangoFilterBackend]
#    filter_fields = ('company',)

#    #def get_permissions(self):    
#    #    #if self.request.method == 'POST' or self.request.method == 'DELETE':
#    #    self.permission_classes = [Isstaff]
#    #    return super(AdViewSet, self).get_permissions()

#class AnalyticsPlatformViewSet(viewsets.ModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = AnalyticsPlatform.objects.all()
#    serializer_class = AnalyticsPlatformSerializer

#class CampaignViewSet(CacheModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = Campaign.objects.all()
#    serializer_class = CampaignSerializer
#    #filter_backends = [DjangoFilterBackend]

#class ChartViewSet(CacheModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = Chart.objects.all()
#    serializer_class = ChartSerializer
#    #filter_backends = [DjangoFilterBackend]

#class ChartStyleViewSet(viewsets.ModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = ChartStyle.objects.all()
#    serializer_class = ChartStyleSerializer

#class ChartTypeViewSet(viewsets.ModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = ChartType.objects.all()
#    serializer_class = ChartTypeSerializer

#class CompanyViewSet(viewsets.ModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = Company.objects.all()
#    serializer_class = CompanySerializer
#    filter_backends = [DjangoFilterBackend, OrderingFilter]
#    filterset_fields = ['company_type', 'is_client', 'is_active', 'name']
#    ordering = ['number', 'name']

#class ContactViewSet(viewsets.ModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = Contact.objects.all()
#    serializer_class = ContactSerializer

#class DataSummaryViewSet(viewsets.ModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = DataSummary.objects.all()
#    serializer_class = DataSummarySerializer
#    filter_backends = [DjangoFilterBackend, OrderingFilter]
#    filterset_fields = ['series', 'series_id', 'series_type',
#                        'entity_id', 'entity_type', 'entity_subtype', 'entity_subtype_id']
#    ordering = ['q1', 'q2', 'q3', 'q4', 'total']

#class DomainViewSet(CacheModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = Domain.objects.all()
#    serializer_class = DomainSerializer
#    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
#    filterset_fields = ['name', 'company__name', 'company__is_client', 'company__number', 'company__company_type', 'asset_tier']
#    search_fields = ['company__name']
#    ordering = ['name', 'company__number']

#class KeywordGroupViewSet(CacheModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = KeywordGroup.objects.all()
#    serializer_class = KeywordGroupSerializer
#    filter_backends = [DjangoFilterBackend]
#    filterset_fields = ['keyword', 'is_free', 'is_core_product', 'related_keyword__is_active', 'related_keyword__is_primary',
#                        'related_keyword__rawExactLocalMonthlySearchVolume', 'related_keyword__rawExactCTR', 'related_keyword__rawExactCostPerClick']

#    def get_serializer_context(self):
#        context = super().get_serializer_context()
#        related_limit = self.request.query_params.get('related_limit', None)
#        if related_limit and related_limit.isdigit() and int(related_limit) > 0:
#            related_limit = int(related_limit)
#        context['related_limit'] = related_limit
#        return context

#    def get_queryset(self):
#        qs = super().get_queryset()
#        qs = qs.prefetch_related(
#            Prefetch('related_keyword', queryset=Keyword.objects.order_by('-clicks')))
#        return qs

#class ParentKeywordViewSet(CacheModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = ParentKeyword.objects.all()
#    serializer_class = ParentKeywordSerializer
#    filter_backends = [DjangoFilterBackend]
#    filterset_fields = ['child_keyword', 'parent_keyword']

#class LocationViewSet(viewsets.ModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = Location.objects.all()
#    serializer_class = LocationSerializer

#class MetricViewSet(viewsets.ModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = Metric.objects.all()
#    serializer_class = MetricSerializer


#class NotificationViewSet(viewsets.ModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = Notification.objects.all()
#    serializer_class = NotificationSerializer

#class MultiReportViewSet(CacheModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = MultiReport.objects.all()
#    serializer_class = MultiReportSerializer
#    filter_backends = [DjangoFilterBackend]
#    filterset_fields = ['name', 'is_active']

#    def get_queryset(self):
#        qs = super().get_queryset()
#        qs = qs.prefetch_related('report')
#        return qs

#class PageViewSet(viewsets.ModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = Page.objects.all()
#    serializer_class = PageSerializer
#    filter_backends = [DjangoFilterBackend, OrderingFilter]
#    filterset_fields = ['url_type', 'keyword_group__keyword', 'keyword_group__is_core_product', 'domain__name']
#    ordering = ['-seo_value_estimate']

#class ReportViewSet(CacheModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = Report.objects.all()
#    serializer_class = ReportSerializer
#    filter_backends = [DjangoFilterBackend]
#    filterset_fields = ['name', 'is_active']

#    def get_queryset(self):
#        qs = super().get_queryset()
#        qs = qs.prefetch_related('chart')
#        return qs

#class RevenueKPIViewSet(viewsets.ModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = RevenueKPI.objects.all()
#    serializer_class = RevenueKPISerializer
#    filter_backends = [DjangoFilterBackend, OrderingFilter]
#    filterset_fields = {'domain__name':['exact', 'isnull'], 'keyword_group__keyword':['startswith', 'isnull'], 'keyword_group__is_core_product':['exact']}
#    ordering = ['-revenue_per_member']

#class SheetViewSet(viewsets.ModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = Sheet.objects.all()
#    serializer_class = SheetSerializer


#class SubscriptionViewSet(viewsets.ModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = Subscription.objects.all()
#    serializer_class = SubscriptionSerializer


#class SubscriptionPlanViewSet(viewsets.ModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = SubscriptionPlan.objects.all()
#    serializer_class = SubscriptionPlanSerializer

#class TestScenarioViewSet(viewsets.ModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = TestScenario.objects.all()
#    serializer_class = TestScenarioSerializer
#    filter_backends = [DjangoFilterBackend, OrderingFilter]
#    filter_fields = ('company__number', 'is_demo', 'is_test', 'is_active')

#class TierViewSet(viewsets.ModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = Tier.objects.all()
#    serializer_class = TierSerializer

#class GlobalSettingViewSet(viewsets.ModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = GlobalSetting.objects.all()
#    serializer_class = GlobalSettingSerializer


#class FAQQuestionViewSet(viewsets.ModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = FAQQuestion.objects.all()
#    serializer_class = FAQQuestionSerializer


#class FAQAnswerViewSet(viewsets.ModelViewSet):
#    permission_classes = [GetOnlyModelPermissions]
#    queryset = FAQAnswer.objects.all()
#    serializer_class = FAQAnswerSerializer

##http://127.0.0.1:8000/preview?cu_id=66584&models=rate_compare&data=car%20loan__rate,5.5__date,2015-01-01|zoo__rate,5.5__date,2015-01-01
#def translate_url_data_to_dict(url_data):
#    data = {}
#    pairs = url_data.split('|')
#    for pair in pairs:
#        product_list = pair.split('__')
#        for i, product in enumerate(product_list):
#            if i==0:
#                data[product] = {}
#            else:
#                k, v = product.split(',')
#                data[product_list[0]][k] = v
#    #print(data)
#    return data

## Charts views
#def demo_chart(request):
#    '''
#    For line chart
#    '''
#    assert isinstance(request, HttpRequest)
#    kwargs = {'period': 'quarterly'}
#    # default value
#    chart_type = 'line'
#    entity, start_year, end_year, all, period = 1, 2018, 2019, True, 'quarterly'

#    entity_get = request.GET.get('entity', None)
#    start_year_get = request.GET.get('start_year', None)
#    chart_type = request.GET.get('chart_type', None)
#    end_year_get = request.GET.get('end_year', None)
#    all_year = request.GET.get("all_year", None)
#    if all_year:
#        all = True

#    if entity_get:
#        kwargs['entity_id'] = entity_get
#    if start_year_get:
#        kwargs['start_year'] = int(start_year_get)
#    if end_year_get:
#        kwargs['end_year'] = int(end_year_get)
#    if chart_type:
#        kwargs['chart_type'] = chart_type
#    # if chart_type == ""
#    data = DataSummary().get_data_(**kwargs)
#    style = ChartType().get_style(chart_type=chart_type)
#    data = chart_utils.update_data(data, style)
#    chart_types = ['line-basic']
#    #data = add_gradient(data)
#    chart_types_dark = ['dark-bar']
#    if chart_type in chart_types:
#        return render(
#            request,
#            'app/charts/dark_chart.html',
#            {'data': json.dumps(data)}
#        )
#    elif chart_type in chart_types_dark:
#        return render(
#            request,
#            'app/charts/dark_bar.html',
#            {'data': json.dumps(data)}
#        )
#    else:

#        style = ChartType().get_style(chart_type=chart_type)
#        #import pdb;pdb.set_trace()
#        data.update(style)
#        return render(
#            request,
#            'app/charts/demo_chart.html',
#            {'data': json.dumps(data)}
#        )
#        # Calculation of growth rate


#def growth_chart(request):
#    growth_types = request.GET

#    return render(
#        request,
#        'app/charts/demo_chart.html',
#        {'data': str(data)}
#    )

#def demo_reports(request):
#    assert isinstance(request, HttpRequest)
#    growth_types = request.GET
#    report_type = "content"
#    report_type = request.GET['report_type']
#    if report_type == "content":
#        return render(
#            request,
#            'app/charts/html/rpt_content_performance.html',
#        )
#    elif report_type == "seo":
#        return render(
#            request,
#            'app/charts/html/rpt_seo_opps.html',
#        )
#    elif report_type == "page":
#        return render(
#            request,
#            'app/charts/html/rpt_page.html',
#        )
#    elif report_type == "page_table":
#        return render(
#            request,
#            'app/charts/html/rpt_page_table.html',
#        )
#    elif report_type == "funnel":
#        return render(
#            request,
#            'app/charts/html/rpt_funnel.html',
#        )


#def static(request):
#    assert isinstance(request, HttpRequest)
#    growth_types = request.GET
#    chart_type = "bar"
#    chart_type = request.GET['chart_type']
#    if chart_type == "area":
#        return render(
#            request,
#            'app/charts/html/area_chart.html',
#        )
#    elif chart_type == "blue_area":
#        return render(
#            request,
#            'app/charts/html/blue_chart.html',
#        )
#    elif chart_type == "pie":
#        return render(
#            request,
#            'app/charts/html/pie_chart.html',
#        )
#    elif chart_type == 'donut':
#        return render(
#            request,
#            'app/charts/html/donut_chart.html'
#        )
#    elif chart_type == "combo":
#        return render(
#            request,
#            'app/charts/html/combo_chart.html',
#        )
#    elif chart_type == "bar":
#        return render(
#            request,
#            'app/charts/html/bar_chart.html',
#        )
#    elif chart_type == "bar_stacked":
#        return render(
#            request,
#            'app/charts/html/bar_stacked_chart.html',
#        )
#    elif chart_type == "bar_stacked_percent":
#        return render(
#            request,
#            'app/charts/html/bar_stacked_percent_chart.html',
#        )
#    elif chart_type == "column":
#        return render(
#            request,
#            'app/charts/html/column_chart.html',
#        )
#    elif chart_type == "column_stacked":
#        return render(
#            request,
#            'app/charts/html/column_stacked_chart.html',
#        )
#    elif chart_type == "column_stacked_percent":
#        return render(
#            request,
#            'app/charts/html/column_stacked_percent_chart.html',
#        )
#    elif chart_type == "funnel":
#        return render(
#            request,
#            'app/charts/html/funnel_chart.html',
#        )
#    elif chart_type == "gauge":
#        return render(
#            request,
#            'app/charts/html/gauge_chart.html',
#        )
#    elif chart_type == "gauge_dynamic":
#        return render(
#            request,
#            'app/charts/html/gauge_dynamic_chart.html',
#        )
#    elif chart_type == "line":
#        return render(
#            request,
#            'app/charts/html/line_chart.html',
#        )
#    elif chart_type == "line_points":
#        return render(
#            request,
#            'app/charts/html/line_points_chart.html',
#        )
#    elif chart_type == 'dumbbell':
#        return render(
#            request,
#            'app/charts/html/dumbbell_chart.html'
#        )
#    elif chart_type == 'dumbbell_vertical':
#        return render(
#            request,
#            'app/charts/html/dumbbell_vertical_chart.html'
#        )
#    elif chart_type == "map":
#        return render(
#            request,
#            'app/charts/html/map_chart.html',
#        )
#    elif chart_type == "map_clusters":
#        return render(
#            request,
#            'app/charts/html/map_clusters_chart.html',
#        )
#    elif chart_type == "map_points":
#        return render(
#            request,
#            'app/charts/html/map_points_chart.html',
#        )
#    elif chart_type == "map_counties":
#        return render(
#            request,
#            'app/charts/html/map_counties_chart.html',
#        )
#    elif chart_type == "test":
#        return render(
#            request,
#            'app/charts/html/test.html',
#        )
#    elif chart_type == 'negative_bar_chart':
#        return render(
#            request,
#            'app/charts/html/negative_bar_chart.html'

#        )
#    elif chart_type == 'single_bar':
#        return render(
#            request,
#            'app/charts/html/single_bar.html'
#        )
#    elif chart_type == 'scatter':
#        return render(
#            request,
#            'app/charts/html/scatter_chart.html'
#        )
#    elif chart_type == 'scatter_3d':
#        return render(
#            request,
#            'app/charts/html/scatter_3d_chart.html'
#        )
#    elif chart_type == 'demo_bar':
#        return render(
#            request,
#            'app/charts/html/demo_bar_chart.html'
#        )
#    elif chart_type == 'demo_line':
#        return render(
#            request,
#            'app/charts/html/demo_line_chart.html'
#        )
#    elif chart_type == 'heatmap':
#        return render(
#            request,
#            'app/charts/html/heatmap_chart.html'
#        )
#    elif chart_type == 'network_graph':
#        return render(
#            request,
#            'app/charts/html/network_graph_chart.html'
#        )
#    elif chart_type == 'sankey':
#        return render(
#            request,
#            'app/charts/html/sankey_chart.html'
#        )
#    elif chart_type == 'wordcloud':
#        return render(
#            request,
#            'app/charts/html/wordcloud_chart.html'
#        )
#    else:
#        template = os.path.join(settings.BASE_DIR,'app/templates/app/charts/modified_html/'+chart_type)
#        if os.path.exists(template):
#            return render(
#                request,
#                template,
#            )
#        else:
#            return JsonResponse({'message':'No chart found'})


## http://localhost:8000/temp?chart_type=blue_area&start_year=2019&end_year=2020


#def temp(request):
#    '''
#    Our temp method takes value from chart type and data summary
#    '''
#    assert isinstance(request, HttpRequest)
#    kwargs = {'period': 'quarterly'}

#    entity_get = request.GET.get('entity_id', None)
#    start_year_get = request.GET.get('start_year', None)
#    chart_type = request.GET.get('chart_type', None)
#    end_year_get = request.GET.get('end_year', None)
#    all_year = request.GET.get("all_year", None)

#    if entity_get:
#        kwargs['entity_id'] = entity_get
#    if start_year_get:
#        kwargs['start_year'] = int(start_year_get)
#    if end_year_get:
#        kwargs['end_year'] = int(end_year_get)
#    if chart_type:
#        kwargs['chart_type'] = chart_type
#    #import pdb;pdb.set_trace()
#    data = DataSummary().get_data_(**kwargs)
#    options = ['bar_dark', 'area', 'blue_area']
#    # if chart_type == "bar":
#    #     chart_type = chart_type + "_dark"
#    #     #import pdb;pdb.set_trace()
#    #     style = ChartType().get_style(chart_type=chart_type)
#    #     updated_data = chart_utils.update_data(data,style)
#    #     return render(
#    #         request,
#    #         'app/charts/blue_chart.html',
#    #         {'data':json.dumps(updated_data)}
#    #     )
#    # if chart_type == "area":
#    #     style = ChartType().get_style(chart_type=chart_type)
#    #     updated_data = chart_utils.update_data(data,style)
#    #     return render(
#    #         request,
#    #          'app/charts/blue_chart.html',
#    #         {'data':json.dumps(updated_data)}
#    #     )
#    # if chart_type == "blue_area":
#    #     style = ChartType().get_style(chart_type=chart_type)
#    #     updated_data = chart_utils.update_data(data,style)
#    #     #import pdb;pdb.set_trace()
#    #     return render(
#    #         request,
#    #         'app/charts/blue_chart.html',
#    #         {'data':json.dumps(updated_data)}
#    #     )
#    if chart_type == "pie":
#        style = ChartType().get_style(chart_type="pie")
#        updated_data = chart_utils.update_pie_chart(data, style)
#        #import pdb;pdb.set_trace()
#        return render(
#            request,
#            'app/charts/blue_chart.html',
#            {'data': json.dumps(updated_data)}

#        )
#    else:
#        style = ChartType().get_style(chart_type=chart_type)
#        updated_data = chart_utils.update_data(data, style)

#        return render(
#            request,
#            'app/charts/blue_chart.html',
#            {'data': json.dumps(updated_data)}
#        )


## Using Chart Model
## @login_required(login_url=admin_login_url)
#def chart_request(request):
#    '''
#    This is for generating the data using chart type
#    '''
#    assert isinstance(request, HttpRequest)
#    chart_id = request.GET.get('chart_id', None)
#    entity_id = request.GET.get('entity_id', None)
#    entity_type = request.GET.get('entity_type', None)
#    entity_subtype_id = request.GET.get('entity_subtype_id', None)
#    entity_subtype = request.GET.get('entity_subtype', None)
#    dimensions = request.GET.get('dimensions', None)
#    map_dimensions = request.GET.get('map', None)
#    start_year = int(request.GET.get('start_year', date.today().year))
#    end_year = int(request.GET.get('end_year', date.today().year))
#    daily_span = request.GET.get('daily_span', None)
#    show_competitors = request.GET.get('show_competitors', None)
#    show_multiple = request.GET.get('show_multiple', False)
#    if chart_id:
#        chart_object = Chart.objects.get(id=chart_id)
#        chart_type = chart_object.charttype.chart_type
#        keywords = {
#            'entity_type': entity_type,
#            'entity_subtype': entity_subtype,
#            'entity_subtype_id': entity_subtype_id,
#            'dimensions': dimensions,
#            'map_dimensions': map_dimensions,
#            'start_year': start_year,
#            'end_year': end_year,
#            'daily_span': daily_span,
#            'show_competitors': True if show_competitors else False,
#            'show_multiple': show_multiple

#        }
#        if entity_id:
#            keywords['entity_id'] = entity_id
#            #TBD the below has been commented out...see if anything breaks
#            #chart_response = chart_object.get_chart(entity_id, entity_type, dimensions, start_year, end_year)
#        updated_data = chart_utils.process_get_chart_data(chart_object, **keywords)
#        # Addition of the style from here
#        if chart_type == 'table':
#            return render(
#                request,
#                'app/charts/table.html',
#                {'data': updated_data}
#            )
#        elif chart_type[:3] == 'map':
#            return render(
#                request,
#                'app/charts/map.html',
#                {'data': updated_data}
#            )
#        elif isinstance(updated_data, list):
#            looping_list = range(0, len(updated_data))
#            return render(
#                request,
#                'app/charts/multiple_charts.html',
#                {'data': json.dumps(updated_data),
#                 'looping_list': looping_list}
#            )
#        else:
#            return render(
#                request,
#                'app/charts/blue_chart.html',
#                {'data': json.dumps(updated_data)}
#            )


#def static_all(request):
#    '''
#    This is for static view for rendering all in one
#    '''
#    return render(
#        request,
#        'app/charts/static.html',
#        # {'data':json.dumps(updated_data)}
#    )

## Wordpress chart


#def wp_example_page(request):
#    return render(
#        request,
#        'app/charts/wp_chart.html',
#        # {'data':json.dumps(updated_data)}
#    )


#def wp_keyword_sample_page(request):
#    return render(
#        request,
#        'app/wp-keywords.html',
#    )

## Dynamic combo chart


#def combo_chart_request(request):
#    chart_one_id = request.GET.get('chart_one_id', '5')
#    entity_id = request.GET.get('entity_id', '24212')
#    start_year = int(request.GET.get('start_year', date.today().year))
#    end_year = int(request.GET.get('end_year', date.today().year))
#    dimensions = request.GET.get('dimensions', None)
#    combo_chart = chart_utils.build_combo_chart(chart_one_id, entity_id, start_year=start_year, end_year=end_year, dimensions=dimensions
#                                                )
#    return render(
#        request,
#        'app/charts/blue_chart.html',
#        {'data': json.dumps(combo_chart)}
#    )

##


#def combine_charts_request(request):
#    kwargs = chart_utils.parse_request_kwargs(request.GET)
#    chart_data = chart_utils.combine_charts(**kwargs)
#    return render(
#        request,
#        'app/charts/blue_chart.html',
#        {'data': json.dumps(chart_data)}
#    )

##New rendering method
#def render_chart_refactor(request):
#    charts_data = chart_builder.get_chart_from_request(request.GET.dict())
#    return render(
#        request,
#        'app/charts/multiple_chart.html',
#        {'data':json.dumps(charts_data)}
#    )


## Wordpress
#def wp(request):
#    return render(
#        request,
#        'app/wp.html',
#        # {'data':json.dumps(updated_data)}
#    )
## Wordpress


#def auth_wp(request):
#    return render(
#        request,
#        'app/wp-auth.html',
#        # {'data':json.dumps(updated_data)}
#    )


#def rankings(request):
#    return render(
#        request,
#        'app/rankings.html',
#        # {'data':json.dumps(updated_data)}
#    )


#def auth_rankings(request):
#    return render(
#        request,
#        'app/auth-rankings.html',
#        # {'data':json.dumps(updated_data)}
#    )


#def analytics2(request):
#    return render(
#        request,
#        'app/analytics.html',
#        # {'data':json.dumps(updated_data)}
#    )


#def auth_analytics(request):
#    return render(
#        request,
#        'app/auth-analytics.html',
#        # {'data':json.dumps(updated_data)}
#    )


#def ncua(request):
#    return render(
#        request,
#        'app/ncua.html',
#        # {'data':json.dumps(updated_data)}
#    )


#def auth_ncua(request):
#    return render(
#        request,
#        'app/auth-ncua.html',
#        # {'data':json.dumps(updated_data)}
#    )


#def ga(request):
#    return render(
#        request,
#        'app/ga.html',
#        # {'data':json.dumps(updated_data)}
#    )


#def auth_ga(request):
#    return render(
#        request,
#        'app/auth-ga.html',
#        # {'data':json.dumps(updated_data)}
#    )


#def ds(request):
#    return render(
#        request,
#        'app/ds.html',
#        # {'data':json.dumps(updated_data)}
#    )


#@login_required(login_url=admin_login_url)
#def auth_ds(request):
#    return render(
#        request,
#        'app/auth-ds.html',
#        # {'data':json.dumps(updated_data)}
#    )


#def membership(request):
#    return render(
#        request,
#        'app/membership.html',
#        # {'data':json.dumps(updated_data)}
#    )


#def auth_membership(request):
#    return render(
#        request,
#        'app/auth-membership.html',
#        # {'data':json.dumps(updated_data)}
#    )


#def cu_report(request):
#    return render(
#        request,
#        'app/cu_report.html',
#        # {'data':json.dumps(updated_data)}
#    )


#def auth_cu_report(request):
#    return render(
#        request,
#        'app/auth_cu_report.html',
#        # {'data':json.dumps(updated_data)}
#    )

#def ptest(request):
#    return render(
#        request,
#        'app/ptest.html',
#    )


#def test_ga_request(request, code='ga'):
#    credentials_dict = request.session['credentials']
#    credentials = google.oauth2.credentials.Credentials(**credentials_dict)
#    ap = AnalyticsPlatform.objects.get(code=code)
#    #http = credentials.authorize(http=httplib2.Http())
#    api = build(ap.api_name, ap.version, credentials=credentials)
#    service = build('analytics', 'v3', credentials=credentials)
#    accounts = service.management().accountSummaries().list().execute()
#    print(accounts)
#    ids = []
#    if accounts.get('items'):
#        for account in accounts['items']:
#            ids.append(account['id'])
#            wad = {}
#            wad['account_id'] = settings.MASTER_ACCOUNT_ID
#            wad['account_type'] = 'ga'
#            wad['external_account_id'] = account['id']
#            wad['token'] = credentials_dict['token']
#            wad['refresh_token'] = credentials_dict['refresh_token']
#            wad['scopes'] = credentials_dict['scopes']
#            wa, created = WebAccount.objects.update_or_create(external_account_id=account['id'], defaults=wad)
#            wt = WebToken(**{'webaccount':wa, 'token':wad['token'], 'refresh_token':wad['refresh_token'], 'ts':int(time.time())}).save()
#            profiles = service.management().profiles().list(accountId=account['id'], webPropertyId='~all').execute()
#            if profiles.get('items'):
#                for prof in profiles['items']:
#                    wpd = {}
#                    wpd['webaccount'] = wa
#                    wpd['external_property_id'] = prof['webPropertyId']
#                    wpd['view_id'] = prof['id']
#                    wpd['name'] = prof['name']
#                    wpd['url'] = prof['websiteUrl']
#                    wp, created = WebProperty.objects.update_or_create(view_id=prof['id'], defaults=wpd)
#                    print(account['id'], prof['webPropertyId'], prof['internalWebPropertyId'], prof['id'], prof['name'], prof['websiteUrl'])

#    print(ids)
#    return JsonResponse(accounts, safe=False)

#def oauth(request):
#    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(os.path.join(settings.BASE_DIR, CLIENT_SECRETS_FILE), scopes=OAUTH_SCOPES)
#    REDIRECT_URI = 'http://127.0.0.1:8000/oauth_callback'
#    #REDIRECT_URI = "https://%s%s" % (get_current_site(request).domain, reverse("oauth2:return"))
#    flow.redirect_uri = REDIRECT_URI
#    authorization_url, state = flow.authorization_url(
#      # Enable offline access so that you can refresh an access token without
#      # re-prompting the user for permission. Recommended for web server apps.
#      access_type='offline',
#      # Enable incremental authorization. Recommended as a best practice.
#      include_granted_scopes='true') #,
#      #OAUTHLIB_INSECURE_TRANSPORT=1)
#    request.session['state'] = state
#    return HttpResponseRedirect(authorization_url)

#def sf_oauth_callback(request):
#    print('sf callback')
#    return JsonResponse({}, status=200)

#def oauth_callback(request):
#    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
#    state = request.session['state']
#    print(state)
#    REDIRECT_URI = 'http://127.0.0.1:8000/oauth_callback'
#    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(os.path.join(settings.BASE_DIR, CLIENT_SECRETS_FILE), scopes=OAUTH_SCOPES, state=state)
#    flow.redirect_uri = REDIRECT_URI
#    authorization_response = request.build_absolute_uri()
#    #authorization_response = 'https' + authorization_response[5:]
#    flow.fetch_token(authorization_response=authorization_response)
#    credentials = flow.credentials
#    request.session['credentials'] = credentials_to_dict(credentials)
#    return HttpResponseRedirect('test_ga_request')

#def credentials_to_dict(credentials):
#  return {'token': credentials.token,
#          'refresh_token': credentials.refresh_token,
#          'token_uri': credentials.token_uri,
#          'client_id': credentials.client_id,
#          'client_secret': credentials.client_secret,
#          'scopes': credentials.scopes}

#class MyAuthenticationBackend(AuthenticationBackend):
#    def authenticate(self, request, **credentials):
#        user = super().authenticate(request, **credentials)
#        userprofile = None
#        print("user", user)
#        if user is not None:
#            userprofile = UserProfile.objects.filter(user=user).first()
#            if userprofile and userprofile.force_password_reset:
#                print("before", userprofile.force_password_reset)
#                days_since_expired = (datetime.now(pytz.timezone(settings.TIME_ZONE)) - userprofile.force_password_reset_date).days
#            # dt = datetime.now() - timedelta(days_inactive)

#                if userprofile.force_password_reset and days_since_expired < 1:
#                    print("password expired first time")
#                    messages.error(request, 'Your password has expired. Please update your password')
#                    print("user authenticated")
#                    return user
#                else:
#                    print("password expired")
#                    #user.set_password(get_random_password(MAX_LEN=35))
#                    #user.save()
#                    messages.error(request,'Your password has expired and has been changed to a random string. Please reset your password.')
#                    #raise ImmediateHttpResponse(HttpResponseRedirect('/accounts/password/reset/'))
#                    raise PermissionDenied("You must change your password. It has expired.")
#        else:
#            return None

#class MySetupCompleteView(SetupCompleteView):
#    def __init__(self, *args,**kwargs):
#        super(MySetupCompleteView, self).__init__(*args,**kwargs)
#    """
#    View congratulate the user when OTP setup has completed.
#    """
#    template_name = 'two_factor/core/setup_complete.html'
#    def get(self, request, *args, **kwargs):
#        user = request.user
#        userprofile = UserProfile.objects.get(user=user)
#        if user and not userprofile.mfa_setup_complete:
#            userprofile.mfa_setup_complete = True
#            userprofile.save()
#        return redirect(settings.LOGIN_REDIRECT_URL)
#        # return super().get(request, *args, **kwargs)
    
#    def get_context_data(self):
#        return {
#            'phone_methods': get_available_phone_methods(),
#        }

#    def dispatch(self, *args, **kwargs):
#         return super(MySetupCompleteView, self).dispatch(*args, **kwargs)
            
#class get_image_lists(View):
#    @method_decorator(login_required(login_url=consumer_login_target_url))
#    @method_decorator((user_passes_test(check_perms, login_url=no_access_url)))
#    @method_decorator(check_mfa_setup)
#    def get(self, request, company_code=None, dir_name=None):
#        error_message = None
#        image_width = request.GET.get("image_width")
#        scraped_company_list = Company.objects.filter(company_type='credit_union').exclude(scrape_demo_base_url=None).order_by('name')

#        if company_code:
#            company = Company.objects.filter(code=company_code).first()
#            file_path = os.path.join('app/static/sites', company.code, company.scrape_demo_base_url)
#            if dir_name:
#                file_path = os.path.join(file_path, dir_name)
#                #dir_search_path = settings.BASE_DIR  + os.sep  + settings.STATICFILES_DIRS[0] + "/sites/" + company_obj.code + os.sep + company_obj.scrape_demo_base_url + os.sep
#                #print(dir_search_path)
#                #get_dir_path = get_dir(fn=dir_name, fp=dir_search_path)
#            #    if dir_search_path is not None:
#            #        file_path = get_dir_path
#            #    else:
#            #        file_path = None
#            #        error_message = "Directory does not exist"
#            #        context = {
#            #            "company_name":company,
#            #            "error_message":error_message,}
#            #        return render(
#            #            request,
#            #            'app/company_image_lists.html',
#            #            context)
#            #else:
#            #    #file_path = settings.BASE_DIR  + os.sep + settings.STATICFILES_DIRS[0] + "/sites/" + company_obj.code + os.sep + company_obj.scrape_demo_base_url + os.sep
#            #    file_path = os.path.join('app/data/sites/', company_obj.code, company_obj.scrape_demo_base_url, dir_name)
#            print(file_path)
#            list_images = traverse_dir(fn='', fp=file_path)
#            image_dict = get_image_dict(list_images)
#            print(image_dict)
#            sorted_image_dict = sorted(image_dict, reverse=True)
#            context = {
#            "company_list":scraped_company_list,
#            "company_name":company,
#            "image_data":sorted_image_dict,
#            }
#            new_image_dict = {}
#            if image_width:
#                for width, width_values in sorted(image_dict.items(), reverse=True):
#                    if int(image_width) == width:
#                        new_image_dict[width]={}
#                        for height,height_values in sorted(width_values.items(), reverse=True):
#                            new_image_dict[width][height] = height_values
                            
#                # image_dict=new_image_dict
#                context = {
#                "company_list":scraped_company_list,
#                "company_name":company,
#                "image_data":new_image_dict,
#                "old_image_data":sorted_image_dict,
#                "image_width":image_width,
#                }
#            return render(
#                request,
#                'app/company_image_lists.html',
#                context)
#        context = {
#            "company_list":scraped_company_list,
#        }
#        print("default context")

#        return render(request, 'app/company_image_lists.html', context)

#def state_zipcodes_func(co, state, locs=None):
#    state_zipcodes = []
#    gs_zipcodes = []
#    states = []
#    selected_states = []
#    gs_data = GlobalSetting.objects.filter(company=co, setting_name="charter_region_counties").first()
#    if gs_data:
#        gs_zipcodes = json.loads(gs_data.setting_value_long)
#        state_zipcodes = ZipCode.objects.filter(state_abbrev=state).values_list('code', flat=True)
#        states = list(set(state_zipcodes.values_list('state_abbrev', flat=True)))
#    else:
#        states = State.objects.all().order_by('name')
#    return gs_zipcodes, state_zipcodes, states

#def add_selected_zipcodes(co, state, selected_counties, zipd):
#    #GlobalSetting.objects.filter(company=co, setting_name="charter_region_zipcodes").update(setting_value_long=json.dumps(temp_gs_zipcodes, separators=(',',' ')))
#    zipcodes = ZipCode.objects.values_list('code', flat=True).filter(state_abbrev=state, county__in=selected_counties).order_by('code')
#    zipcodes = list(set(zipcodes))
#    zipd[state] = zipcodes
#    gs, created = GlobalSetting().saveGS('charter_region_zipcodes', zipd, co=co)

#def add_selected_counties(co, state, selected_counties, countyd):
#    #GlobalSetting.objects.filter(company=co, setting_name="charter_region_counties").update(setting_value_long=json.dumps(selected_counties, separators=(',',' ')), status=1)
#    countyd[state] = selected_counties
#    gs, created = GlobalSetting().saveGS('charter_region_counties', countyd, co=co)

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def setting_charter_region(request):
#    template = 'admin/settings/charter_region.html'
#    message = None
#    context = {}
#    companies = []
#    countyd = {}
#    zipd = {}
#    cu_id = request.GET.get('cu_id')
#    state = request.GET.get('state', '')
#    context['state'] = state
#    last_state = request.session.get('last_state')
#    request.session['last_state'] = state
#    selected_states = request.session.get('selected_states', [])
#    selected_counties = request.session.get('selected_counties', [])
#    selected_zipcodes = request.session.get('selected_zipcodes', [])

#    if not request.user.is_superuser:
#        cu_id = request.user.userprofile.company.number
#    if cu_id:
#        request.session['cu_id'] = cu_id
#    co = Company().get_company(cu_id, 'number')

#    gs_status_exists = GlobalSetting.objects.filter(company=co, setting_name='charter_region_status').exists()
#    if gs_status_exists:
#        lg.info('settings already exist')
#        countyd = json.loads(GlobalSetting.objects.filter(company=co, setting_name='charter_region_counties').first().setting_value_long)
#        zipd = json.loads(GlobalSetting.objects.filter(company=co, setting_name='charter_region_zipcodes').first().setting_value_long)
#        lg.info(('cd gs exists', countyd))

#        #selected_states = list(countyd.keys())
#        selected_counties = []
#        selected_zipcodes = []
#        selected_states = request.session.get('selected_states', [])
#        request.session['selected_counties'] = selected_counties
#        request.session['selected_zipcodes'] = selected_zipcodes

#    if request.method == 'POST':
#        lg.info('data posted')
#        lg.info(('state', state))
#        lg.info(('ss', selected_states))
#        lg.info(('sc', selected_counties))
#        if not state:
#            lg.info('no selected states or counties')
#            selected_states = request.POST.getlist('chkbox')
#            print('input selected_states', selected_states)
#            request.session['selected_states'] = sorted(selected_states)
#            return redirect('/b/ai-settings/charter-region?cu_id=' + cu_id + '&state=' + selected_states[0])
#        elif selected_states and not selected_counties:
#            lg.info('selected states but not counties')
#            selected_counties = request.POST.getlist('chkbox')
#            context['selected_states'] = selected_counties
#            print('selected_counties', selected_counties)
#            request.session['selected_counties'] = selected_counties

#        if state and request.session.get('last_state') != None:
#            print('last state')
#            lg.info('state and last_state')
#            gs_zipcodes, state_zipcodes, states = state_zipcodes_func(co, state)
#            add_selected_counties(co, state, selected_counties, countyd)
#            add_selected_zipcodes(co, state, selected_counties, zipd)
#            gs_status, created = GlobalSetting().set_status(co, 'charter_region_status', '1')
#            # print('state_zipcodes2', state_zipcodes)
#            if last_state == selected_states[-1]:
#                request.session['last_state'] = None
#                return redirect('/b/ai-settings/charter-region?cu_id=' + cu_id)
#            else:
#                next_state_index = selected_states.index(state) + 1
#                return redirect('/b/ai-settings/charter-region?cu_id=' + cu_id + '&state=' + selected_states[next_state_index])

#        else:
#            state = selected_states[0]
#            countyd[state] = selected_counties
#            lg.info(('cd', countyd))
#            gs, created = GlobalSetting().saveGS('charter_region_counties', countyd, co=co)

#            gskwargs = {
#                'company':co,
#                'setting_name':'charter_region_counties',
#                'setting_value_long':json.dumps(countyd),
#                }

#            gs_crc, created = GlobalSetting.objects.update_or_create(company=co, setting_name='charter_region_counties', defaults=gskwargs)

#            zipcodes = ZipCode.objects.values_list('code', flat=True).filter(state_abbrev=state, county__in=selected_counties)
#            zipcodes = list(set(zipcodes))
#            zipd[state] = zipcodes

#            gskwargs['setting_name'] = 'charter_region_zipcodes'
#            gskwargs['setting_value_long'] = json.dumps(zipd)
#            gs_crz, created = GlobalSetting.objects.update_or_create(company=co, setting_name='charter_region_zipcodes', defaults=gskwargs)

#            gs_status, created = GlobalSetting().set_status(co, 'charter_region_status', '1')
#            #distinct_states = list(ZipCode.objects.filter(code__in=zipcodes).values_list('state_abbrev', flat=True).distinct())
#            #request.session['distinct_states'] = distinct_states
#            #return redirect('/b/ai-settings/charter-region?cu_id=' + cu_id + '&state=' + distinct_states[0])
#            return redirect('/b/ai-settings/charter-region?cu_id=' + cu_id + '&state=' + state)

#    elif cu_id:
#        counties = County.objects.filter(state_abbrev=state).order_by('name')
#        states = State.objects.all().order_by('state_abbrev')
#        context['counties'] = counties
#        if countyd and (not state or state in countyd):
#            context['selected_states'] = list(countyd.keys())
#            if countyd.get(state):
#                selected_counties = countyd[state]
#        else:
#            locs = Location.objects.filter(company=co)
#            locs_state = Location.objects.filter(company=co, physicaladdressstatecode=state)
#            gs_zipcodes, state_zipcodes, states = state_zipcodes_func(co, state, locs)
#            selected_counties = list(set(locs_state.values_list('physicaladdresscountyname', flat=True)))
#            if state:
#                charter_zipcodes = ZipCode.objects.filter(state_abbrev=state)
#                print('state_zipcodes', state_zipcodes)
#                context['selected_zipcodes'] = list(state_zipcodes)
#                context['selected_states'] = list(selected_states)
#            else:
#                if gs_zipcodes:
#                    selected_zipcodes = gs_zipcodes
#                else:
#                    selected_zipcodes = list(set(locs_state.values_list('physicaladdresspostalcode', flat=True)))
#                    states_in_charter = list(set(locs.values_list('physicaladdressstatecode', flat=True)))
#                    #charter_zipcodes = ZipCode.objects.filter(state_abbrev__in=states_in_charter)
#                    context['selected_states'] = states_in_charter
#                context['selected_zipcodes'] = selected_zipcodes
#        context['selected_counties'] = selected_counties
#        #context['charter_zipcodes'] = charter_zipcodes
#        context['states'] = states
#        #print(gs_zipcodes)
#        print(selected_states)
#        print(sorted(selected_counties))
#        print(state)
#    elif not cu_id:
#        if request.user.is_superuser:
#            companies = Company.objects.filter(company_type='credit_union', is_subscriber=True).order_by('name')
#            context['companies'] = companies

#    return render(request, template, context)    


#def select_all_states():
#    temp_selected_states = []
#    fp = 'app/static/app/assets/js/plugin/highcharts/maps/mapdata/countries/us/'
#    fn = 'us-all.topo.json'
#    if path_exists(fn, fp):
#        data = load_file(fn, fp)
#        d = json.loads(data)
#        for i in d['objects']['default']['geometries']:
#            temp_selected_states.append(i['properties']['hc-a2'])
#    return temp_selected_states

#def select_all_counties(state):
#    temp_selected_states = []
#    fp = 'app/static/app/assets/js/plugin/highcharts/maps/mapdata/countries/us/'
#    fn = 'us-%s-all.topo.json'%state.lower()
#    if path_exists(fn, fp):
#        data = load_file(fn, fp)
#        # print(json.loads(data))
#        d = json.loads(data)
#        for i in d['objects']['default']['geometries']:
#            temp_selected_states.append(i['properties']['name'])
#    return temp_selected_states

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def charter_region_map(request):
#    from django.contrib import messages
#    context = {}
#    context['template'] = 'admin/settings/charter_region_map.html'
#    message = None
    
#    companies = []
#    countyd = {}
#    zipd = {}
#    cu_id = request.GET.get('cu_id')
#    state = request.GET.get('state', '')
#    select = request.GET.get('select', '')
#    context['state'] = state
#    last_state = request.session.get('last_state')
#    request.session['last_state'] = state
#    selected_states = request.session.get('selected_states', [])
#    selected_counties = request.session.get('selected_counties', [])
#    selected_zipcodes = request.session.get('selected_zipcodes', [])

#    co, ugs, context = check_company(request, context)
#    # if context['is_fin_employee'] and not context['cu_id']:
#    #     return redirect(reverse('choose-company'))
#    #if not request.user.is_superuser:
#    #    cu_id = request.user.userprofile.company.number
#    #if cu_id:
#    #    request.session['cu_id'] = cu_id
#    #co = Company().get_company(cu_id, 'number')

#    gs_status_exists = GlobalSetting.objects.filter(company=co, setting_name='charter_region_status').exists()
#    if gs_status_exists:
#        lg.info('settings already exist')
#        countyd = json.loads(GlobalSetting.objects.filter(company=co, setting_name='charter_region_counties').first().setting_value_long)
#        zipd = json.loads(GlobalSetting.objects.filter(company=co, setting_name='charter_region_zipcodes').first().setting_value_long)
#        lg.info(('cd gs exists', countyd))

#        #selected_states = list(countyd.keys())
#        selected_counties = []
#        selected_zipcodes = []
#        selected_states = request.session.get('selected_states', [])
#        request.session['selected_counties'] = selected_counties
#        request.session['selected_zipcodes'] = selected_zipcodes

#    if request.method == 'POST':
#        lg.info('data posted')
#        lg.info(('state', state))
#        lg.info(('ss', selected_states))
#        lg.info(('sc', selected_counties))
#        if not state:
#            lg.info('no selected states or counties')
#            selected_states = request.POST.get('chkbox')
#            selected_states = selected_states.split(',')
#            if countyd:
#                GlobalSetting().remove_unselected_existing_states(co, 'charter_region_counties', selected_states, countyd)            
#            request.session['selected_states'] = sorted(selected_states)
#            return redirect(reverse('charter') + '?cu_id=' + co.number + '&state=' + selected_states[0])
#        elif selected_states and not selected_counties:
#            lg.info('selected states but not counties')
#            selected_counties = request.POST.get('chkbox')
#            selected_counties = selected_counties.split(',')
#            context['selected_states'] = selected_counties
#            request.session['selected_counties'] = selected_counties

#        if state and request.session.get('last_state') != None:
#            lg.info('state and last_state')
#            gs_zipcodes, state_zipcodes, states = state_zipcodes_func(co, state)
#            add_selected_counties(co, state, selected_counties, countyd)
#            add_selected_zipcodes(co, state, selected_counties, zipd)
#            gs_status, created = GlobalSetting().set_status(co, 'charter_region_status', '1')
#            # print('state_zipcodes2', state_zipcodes)
#            if last_state == selected_states[-1]:
#                request.session['last_state'] = None
#                messages.success(request, 'Your settings have been saved.')
#                return redirect(reverse('charter') + '?cu_id=' + co.number)
#            else:
#                next_state_index = selected_states.index(state) + 1
#                return redirect(reverse('charter') + '?cu_id=' + co.number + '&state=' + selected_states[next_state_index])

#        else:
#            state = selected_states[0]
#            countyd[state] = selected_counties
#            lg.info(('cd', countyd))
#            gs, created = GlobalSetting().saveGS('charter_region_counties', countyd, co=co)

#            gskwargs = {
#                'company':co,
#                'setting_name':'charter_region_counties',
#                'setting_value_long':json.dumps(countyd),
#                }

#            gs_crc, created = GlobalSetting.objects.update_or_create(company=co, setting_name='charter_region_counties', defaults=gskwargs)

#            zipcodes = ZipCode.objects.values_list('code', flat=True).filter(state_abbrev=state, county__in=selected_counties)
#            zipcodes = list(set(zipcodes))
#            zipd[state] = zipcodes

#            gskwargs['setting_name'] = 'charter_region_zipcodes'
#            gskwargs['setting_value_long'] = json.dumps(zipd)
#            gs_crz, created = GlobalSetting.objects.update_or_create(company=co, setting_name='charter_region_zipcodes', defaults=gskwargs)

#            gs_status, created = GlobalSetting().set_status(co, 'charter_region_status', '1')
#            return redirect(reverse('charter') + '?cu_id=' + co.number + '&state=' + state)

#    elif context['cu_id'] and not context['cu_id'] == 'all' and co:
#        counties = County.objects.filter(state_abbrev=state).order_by('name')
#        states = State.objects.all().order_by('state_abbrev')
#        context['counties'] = counties
#        if not state and select:
#            if select == 'select_all':
#                context['selected_states'] = ','.join(select_all_states())
#            elif select == 'deselect_all':
#                context['selected_states'] = []        
#        elif state and select:
#            if select == 'select_all':
#                selected_counties = select_all_counties(state)
#            elif select == 'deselect_all':
#                selected_counties = []            
#        elif countyd and (not state or state in countyd):
#            context['selected_states'] = ','.join(list(countyd.keys()))
#            if countyd.get(state):
#                selected_counties = countyd[state]
#        else:
#            locs = Location.objects.filter(company=co)
#            locs_state = Location.objects.filter(company=co, physicaladdressstatecode=state)
#            gs_zipcodes, state_zipcodes, states = state_zipcodes_func(co, state, locs)
#            selected_counties = list(set(locs_state.values_list('physicaladdresscountyname', flat=True)))
#            if state:
#                charter_zipcodes = ZipCode.objects.filter(state_abbrev=state)
#                context['selected_zipcodes'] = list(state_zipcodes)
#                context['selected_states'] = list(selected_states)
                
#            else:
#                if gs_zipcodes:
#                    selected_zipcodes = gs_zipcodes
#                else:
#                    selected_zipcodes = list(set(locs_state.values_list('physicaladdresspostalcode', flat=True)))
#                    states_in_charter = list(set(locs.values_list('physicaladdressstatecode', flat=True)))
#                    #charter_zipcodes = ZipCode.objects.filter(state_abbrev__in=states_in_charter)
#                    context['selected_states'] = ','.join(states_in_charter)
                    
                    
#                context['selected_zipcodes'] = selected_zipcodes
    
        
#        context['selected_counties'] = ','.join(selected_counties)
#        #context['charter_zipcodes'] = charter_zipcodes
#        context['states'] = states
#    # elif not co:
#        # if request.user.is_superuser:
#        #     companies = Company.objects.filter(company_type='credit_union', is_subscriber=True).order_by('name')
#        #     context['companies'] = companies
#        # return redirect(reverse('charter')+'?cu_id='+context['cu_id'])
#    return render(request, context['template'], context)

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def branch_events(request):
#    template = 'admin/branch-events.html'
#    context = {}
#    co, ugs, context = check_company(request, context)
#    return render(request, template, context)

#def create_zc_json(request):
#    # url = "https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/ga_georgia_zip_codes_geo.min.json"
#    # url = "https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/fl_florida_zip_codes_geo.min.json"
    
#    params = {}
#    # r = requests.get(url)
#    # file_path = "app/static/app/assets/js/plugin/highcharts/maps/mapdata/countries/us/states/state-zips/ga_georgia_zip_codes_geo.min.json"
    
#    # r_json = r.json()
#    file_names = os.listdir("app/static/app/assets/js/plugin/highcharts/maps/mapdata/countries/us/states/state-zips")
    

#    for file_name in file_names:
#        file_path = "app/static/app/assets/js/plugin/highcharts/maps/mapdata/countries/us/states/state-zips/%s"%file_name
#        # file_path = "app/static/app/assets/js/plugin/highcharts/maps/mapdata/countries/us/states/state-zips/nh_new_hampshire_zip_codes_geo.min.json"
#        r = open(file_path, "r")
#        state_abbrev = file_path.split("/")[-1].split("_")[0]
#        print('state', state_abbrev)
#        r_json = json.load(r)
#        for ind, i in enumerate(r_json['features']):
#            params["type"] = i['type']
#            params["properties"] = i['properties']
#            ZipCode.objects.filter(code=i['properties']['ZCTA5CE10']).update(geo_state = i['properties']['STATEFP10'], geo_id = i['properties']['GEOID10'], land_area = i['properties']['ALAND10'], water_area = i['properties']['AWATER10'], total_area = i['properties']['ALAND10'] + i['properties']['AWATER10'], water_per = None, land_per = None)
#            if ZipCode.objects.filter(code=i['properties']['ZCTA5CE10']):
#                i['properties']['CITY'] = ZipCode.objects.filter(code=i['properties']['ZCTA5CE10']).first().city
#            else:
#                i['properties']['CITY'] = None
#                lg.info('zipcode missing in zipcode table')
#                lg.info(i['properties']['ZCTA5CE10'])
#            i['properties']['CITY'] = ZipCode.objects.filter(code=i['properties']['ZCTA5CE10']).first().city if ZipCode.objects.filter(code=i['properties']['ZCTA5CE10']) else None
#            params["geometry"] = i['geometry']
#            # path = 'app/data/geojson/%s'%state_abbrev
#            path = 'app/static/app/assets/js/plugin/highcharts/maps/mapdata/geojson/%s'%state_abbrev
#            if not os.path.exists(path):
#                t_path = os.path.join('app/static/app/assets/js/plugin/highcharts/maps/mapdata/geojson', state_abbrev)
#                os.mkdir(t_path)
#            # full_file_path = "%s%s"%(dir_path, i['properties']['ZCTA5CE10'])
#            f = open(f"{path}/{i['properties']['ZCTA5CE10']}.json", "w")
#            f.write(json.dumps(params))
#            f.close()
#    return JsonResponse({'status':1, 'params': params})

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def create_branch_event(request):
#    template = 'admin/create-branch-events.html'
#    message = None
#    context = {}
#    companies = []
#    co, ugs, context = check_company(request, context)
#    if request.method == 'POST':
#        zipcode = request.POST['zipcode']
#        request.session['zipcode'] = zipcode

#        if request.user.is_superuser:
#            cu_id = request.POST['cu_id']
#        else:
#            cu_id = request.user.userprofile.company.number

#        request.session['cu_id'] = cu_id

#        z = ZipCode.objects.filter(code=zipcode).first()
#        if not z:
#            message = "Zipcode does not exist."
#            context = {'message': message}
#        else:
#            return redirect(reverse('list_counties'))
            
#    else:
#        if request.user.is_superuser:
#            companies = Company().get_subscribers()
#            context['companies'] = companies

#    return render(request, template, context)    

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def list_counties(request):
#    from pmodels import distance_pm_zipcodes
#    template = 'admin/list-counties.html'
#    cu_id = request.session.get('cu_id')
#    zipcode = request.session.get('zipcode')
#    context = {}
#    co, ugs, context = check_company(request, context)
#    co = Company.objects.filter(number=cu_id).first()
#    zc = ZipCode.objects.filter(code=zipcode).first()

#    if not request.user.is_superuser:
#        cu_id = request.user.userprofile.company.number
#    if cu_id:
#        request.session['cu_id'] = cu_id
#    co = Company().get_company(cu_id, 'number')
#    if request.method == 'POST':
#        #ad = Ad()
#        #ad.company = co
#        #ad.save()
#        #request.session['ad_id'] = ad.id
#        selected_zipcodes = request.POST.get('chkbox')
#        selected_zipcodes = selected_zipcodes.split(',')
        
#        request.session['selected_zipcodes'] = sorted(selected_zipcodes)
#        return redirect(reverse('zipcodes_template_selection'))
#    else:
#        selected_zipcodes = []
#        if co and GlobalSetting.objects.filter(company=co, setting_name="charter_region_zipcodes"):
#            gs_zipcodes = GlobalSetting.objects.filter(company=co, setting_name="charter_region_zipcodes").first()
#            temp_zips = json.loads(gs_zipcodes.setting_value_long)
#            folder_paths = list(temp_zips.keys())
#            zips = list(json.loads(gs_zipcodes.setting_value_long).values())
#            charter_zipcode_list = []
#            for ind, l in enumerate(zips):
#                charter_zipcode_list += l
#            charter_zipcodes = ZipCode.objects.filter(code__in=charter_zipcode_list).order_by('code')
#            #C:\Source\Repos\ga\app\static\app\assets\js\plugin\highcharts\maps\mapdata\
#            existing_zipcodes_arr = []
#            local_zipcodes = distance_pm_zipcodes(zipcode=zc.code, threshold=60, latlong=(zc.latitude, zc.longitude), zipcodes=charter_zipcodes)
#            print('local_zipcodes len', len(local_zipcodes))
#            for single_zipcode in local_zipcodes:
#                fn = '%s.json'%single_zipcode
#                for folder_name in folder_paths:
#                    fp = 'app/static/app/assets/js/plugin/highcharts/maps/mapdata/geojson/' + folder_name.lower()
#                    if path_exists(fn, fp):
#                        data = load_file(fn, fp)
#                        existing_zipcodes_arr.append(json.loads(data))
#                        break
#                    else:
#                        lg.info('missing zip: ' + single_zipcode)

#            geojson = {"type": "FeatureCollection", "features": existing_zipcodes_arr}
#            context['charter_zipcodes'] = json.dumps(geojson)
#            thirty_miles_zipcodes = distance_pm_zipcodes(zipcode=zc.code, threshold=30, latlong=(zc.latitude, zc.longitude), zipcodes=charter_zipcodes)
#            for z in thirty_miles_zipcodes:
#                if z in charter_zipcode_list:
#                    selected_zipcodes.append(z)
#            if zipcode not in selected_zipcodes:
#                selected_zipcodes.append(zipcode)
#            context['selected_zipcodes'] = json.dumps(selected_zipcodes)

#    return render(request, template, context)


#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def zipcodes_template_selection(request):
#    template = 'admin/zipcodes-template-selection.html'
#    context = {}
#    cu_id = request.session.get('cu_id')
#    co, ugs, context = check_company(request, context)
#    co = Company.objects.filter(number=cu_id).first()
#    if request.method == 'POST':
#        ad_template_id = int(request.POST.get('ad_template', 0))
#        if ad_template_id:
#            ad_template = AdTemplate.objects.get(id=ad_template_id)
#            context['ad_template'] = ad_template
#            request.session['ad_template_id'] = ad_template.id
#        else:
#            ad_html = request.POST['ad_html']
#            lg.info(ad_html)
#            ad_template = AdTemplate.objects.get(id=request.session.get('ad_template_id'))
#            #ad_id = request.session.get('ad_id')
#            data = {
#                    #'id':ad_id,
#                   'company':co,
#                   'content_type':'branch',
#                   'category':'geo',
#                   'subcategory':'zipcode',
#                   'is_active':False,
#                   'is_dynamic':True,
#                   'pages':ad_template.pages,
#                   'ad_method':ad_template.ad_method,
#                   'delivery_type':ad_template.delivery_type,
#                   'div_id':ad_template.div_id,
#                   'div_class':ad_template.div_class,
#                   'div_type':ad_template.div_type,
#                   'ordinal':ad_template.ordinal,
#                   'ad_template':ad_template,
#                   'ad_html':ad_html,
#                   }
#            request.session['ad_dict'] = data
#            return redirect(reverse('ad_settings'))
#    else:
#        ad_templates = AdTemplate.objects.filter(company=co).order_by('template_name')
#        context['data'] = ad_templates

#    return render(request, template, context)

#def process_form(request):
#    data = request.POST.copy()
#    data.pop('csrfmiddlewaretoken', None)
#    print('pop csrf')
#    for k, v in data.items():
#        if isinstance(v, list):
#            print(k, v)
#            if v[0] == '':
#                data[k] = None
#            else:
#                data[k] = v[0]
#    return data

#def remove_empty_keys(data):
#    keys = list(data.keys())
#    for k in keys:
#        if not data[k]:
#            data.pop(k, None)
#    return data

#def clear_session(request, include=[], exclude=[]):
#    for key in list(request.session.keys()):
#        #print(key)
#        if key not in exclude and key in include:
#            del request.session[key]

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def ad_settings(request):
#    template = 'admin/ad_settings.html'
#    from django.contrib import messages
#    context = {}
#    co, ugs, context = check_company(request, context)
#    data = remove_empty_keys(request.session.get('ad_dict'))
#    context['form'] = data
#    if request.method == 'POST':
#        form_data = request.POST.dict()
#        ad_dict = request.session.get('ad_dict')
#        selected_zipcodes = request.session.get('selected_zipcodes')
#        data = dict(data, **form_data)
#        ad_id = None
#        #if 'id' in data:
#        #    ad_id = data['id']
#        if data.get('is_active') == 'on':
#            data['is_active'] = True
#        if data.get('csrfmiddlewaretoken'):
#            data.pop('csrfmiddlewaretoken', None)
#        if 'start_dt' in data:
#            data.pop('start_dt', None)
#        if 'end_dt' in data:
#            data.pop('end_dt', None)
#        data = dict(ad_dict, **data)
#        ad, created = Ad.objects.update_or_create(id=ad_id, defaults=data)
#        #clear_session(request, include=['zipcode', 'cu_id', 'ad_template_id', 'ad_dict'])
#        for z in selected_zipcodes:
#            data = {
#                'company':ad.company,
#                'setting_category':'geo',
#                'setting_subcategory':'zipcode',
#                'setting_name':('%s.ad.%s')%(z, ad.id),
#                'setting_value':0.9,
#                'add_to_pconfig': True
#                }
#            #GlobalSetting(**data).save()
#            gs, created = GlobalSetting().gs_update_or_create(data)
#        messages.success(request, 'New scenario created!')
#        return redirect(reverse('content-modules'))
#    else:
#        context['ad_method'] = AD_METHOD
#        context['delivery_types'] = DELIVERY_TYPES
#    lg.info(data)
#    return render(request, template, context)

#def save_category(co, cat_type, cat_value, segment, single_item=True):
#    subcategory = None
#    if single_item:
#        if segment:
#            subcategory = 'segments'
#            cat_value = "%s|%s"%(cat_value,segment)
#    else:
#        subcategory = "%s.%s"%(cat_type, cat_value)
#        if segment:
#            cat_value = "segments.%s"%segment
#        else:
#            cat_value = None
#        cat_type = "demographics"
#    q = GlobalSetting.objects.filter(company=co, setting_category= cat_type)
#    if q:
#        # as you asked me last time to use save() function instead of update, it was giving me issue "argument of type 'NoneType' is not iterable" by using save()
#        # q = GlobalSetting.objects.filter(company=co, setting_category= cat_type).first()
#        # q.setting_subcategory = subcategory
#        # q.setting_value = cat_value
#        # q.add_to_pconfig = True
#        # q.save()

#        q.update(setting_subcategory = subcategory, setting_value = cat_value,add_to_pconfig = True)

#    else:
#        q=GlobalSetting(company=co, setting_category = cat_type, setting_subcategory = subcategory, setting_value = cat_value, add_to_pconfig = True)
#        q.save()

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def list_ads_for_segment(request):
#    template = 'admin/list-ads-for-segment.html'
#    ad_images = []
#    context = {}
#    co, ugs, context = check_company(request, context)
#    cu_id = request.GET.get('cu_id')
#    if not request.user.is_superuser:
#        cu_id = request.user.userprofile.company.number
#    if cu_id:
#        request.session['cu_id'] = cu_id
#        co = Company().get_company(cu_id, 'number')
#        ads = Ad.objects.filter(company=co).order_by('-timestamp_modified')
#        for ad in ads:
#            ad_images.append(get_ad_first_image(ad.company, [ad]))

#        context = {
#            'ads': zip(ad_images, ads)
#        }        
#    elif not cu_id:
#        if request.user.is_superuser:
#            companies = Company().get_subscribers()
#            context['companies'] = companies    


#    return render(request, template, context)

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def replace_img_url_segment(request):
#    from pmodels import get_ad_images
#    template = 'admin/replace-img-url-segment.html'
#    context = {}
#    ad_arr = []
#    co, ugs, context = check_company(request, context)
#    cu_id = request.session.get('cu_id')
#    if not request.user.is_superuser:
#        cu_id = request.user.userprofile.company.number
#    if cu_id:
#        request.session['cu_id'] = cu_id

#    co = Company().get_company(cu_id, 'number')
#    ad_id = request.GET['ad_ids'] if 'ad_ids' in request.GET else None
    
#    if request.method == 'POST':
#        img_path_radio = request.POST['img_path_radio'] if 'img_path_radio' in request.POST else None
#        if img_path_radio:
#            ad = Ad.objects.get(id=int(ad_id))
#            ad.img_to_replace = img_path_radio
#            ad.save()
#        return redirect(reverse('upload_img_segment')+'?ad_ids=%s'%ad_id)

#    ad = Ad.objects.filter(id=ad_id).first()
#    if not ad:
#        context['message'] = 'Ad does not exist.'
#    else:
#        ad_arr.append(ad)
#        imgs_path_arr = get_ad_images(co, ad_arr, exclude_assets=True)
#        if len(imgs_path_arr) == 1:
#            ad.img_to_replace = imgs_path_arr[0]
#            ad.save()
#            return redirect(reverse('upload_img_segment')+'?ad_ids=%s'%ad.id)
#        context['imgs_path_arr'] = imgs_path_arr

#    return render(request, template, context)

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def upload_img_segment(request):
#    from file_tools import upload_file
#    from pmodels import check_url_start
#    from django.core.files.storage import FileSystemStorage
#    template = 'admin/upload-img-segment.html'
#    context = {}
#    co, ugs, context = check_company(request, context)
#    cu_id = request.session.get('cu_id')
#    if not request.user.is_superuser:
#        cu_id = request.user.userprofile.company.number
#    if cu_id:
#        request.session['cu_id'] = cu_id

#    co = Company().get_company(cu_id, 'number')
#    ad_id = request.GET.get('ad_ids', None)
#    asset_id = request.GET.get('asset_id', '')
#    if request.method == 'POST':
#        enabled_tab = request.POST.get('enabled_tab', None)
#        ad = Ad.objects.filter(id=int(ad_id)).first()
#        if ad:
#            domain = Domain.objects.filter(company=co).first()
#            next_url = 'choose_targeted_segment'
#            asset_kwargs = {
#                'company':co,
#                'domain':domain,
#                }
#            if enabled_tab == 'upload':
#                #base_url = 'http://127.0.0.1:8001'
#                base_url = settings.IMG_STORE_BASE_URL
#                file_obj = request.FILES.getlist('file')[0]
#                path = '%s/media/%s'%(settings.BASE_DIR, co.code)
#                file_name = upload_file(co, file_obj, path).split('/')[-1]
#                asset_kwargs['url'] = '%s/media/%s/%s'%(base_url, co.code, file_name)
#                asset_kwargs['short_url'] = '%s/media/%s/%s'%(base_url, co.code, file_name)
#                asset_kwargs['filename'] = file_name
#                next_url = 'upload_img_segment'
#            elif enabled_tab == 'img_url':
#                inp_img_url = request.POST.get('inp_img_url', None)
#                if inp_img_url:
#                    if check_url_start(inp_img_url, ['http']) and not inp_img_url.startswith('/'):
#                        inp_img_url = '/%s'%inp_img_url
#                    asset_kwargs['url'] = inp_img_url
#                    asset_kwargs['short_url'] = inp_img_url
#                    asset_kwargs['filename'] = inp_img_url.split('/')[-1]
#            #elif enabled_tab == 'media_library':
#            #    return redirect(reverse('choose_targeted_segment')+'?ad_ids=%s'%ad_id)

#            asset_crc, created = Asset.objects.update_or_create(company=co, domain=domain, url=asset_kwargs.get('url'), defaults=asset_kwargs)
#            if asset_crc:
#                asset_id = asset_crc.id
#                request.session['asset_id'] = asset_id
#            return redirect(reverse(next_url)+'?ad_ids=%s&asset_id=%s'%(ad_id, asset_id))

#    else:
#        list_images = Asset.objects.values('short_url').filter(company=co).order_by('-timestamp_modified')
#        for imgs in list_images:
#            url = imgs['short_url'].replace('/app/', '/')
#            if co.code == 'vys':
#                url = '/static/sites/'+ co.code + '/www.stgfinalyticsdemo.com' + imgs['short_url']
#            elif co.scrape_demo_base_url and '/static/sites/' not in imgs['short_url']:
#                url = '/static/sites/'+ co.code + '/' + co.scrape_demo_base_url + imgs['short_url']	
#            # print(url)        
    
#    context['ad_id'] = ad_id
#    context['asset_id'] = asset_id
#    return render(request, template, context)

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def choose_targeted_segment(request):
#    template = 'admin/choose-targeted-segment.html'
#    context = {}
#    kg_list = []
#    cu_id = request.session.get('cu_id')
#    co, ugs, context = check_company(request, context)
#    if not request.user.is_superuser:
#        cu_id = request.user.userprofile.company.number
#    if cu_id:
#        request.session['cu_id'] = cu_id    

#    co = Company().get_company(cu_id, 'number')
#    ad_id = request.GET.get('ad_ids', None)
    
#    if request.method == 'POST':
#        targeted_segment = request.POST.get('targeted_segment', None)
#        # targeted_segment = KeywordGroup.objects.filter(id=targetted_segment_id).first()
#        asset_id = request.session.get('asset_id', '')
#        if asset_id:
#            del request.session['asset_id']

#        ad = Ad.objects.filter(id=int(ad_id)).first()
#        if ad:
#            domain = Domain.objects.filter(company=co).first()
#            a = Asset.objects.filter(id=int(asset_id)).first()
#            if a:
#                a.demographics = append_to_str_list(a.demographics, targeted_segment)
#                a.keyword_group = ad.keyword_group
#                a.is_active = ad.is_active
#                a.is_biz = ad.is_biz
#                a.div_ids = ad.div_id
#                a.div_classes = ad.div_class
#                a.content_type = ad.content_type
#                a.category = ad.category
#                a.subcategory = ad.subcategory
#                a.pages = ad.pages
#                a.save()
#                return redirect(reverse('setup_complete_segment')+'?ad_ids=%s&asset_id=%s'%(ad_id, asset_id))

#    kg_list = KeywordGroup.objects.filter(category='segment').order_by('keyword')
#    context['kg_list'] = kg_list

#    return render(request, template, context)

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def setup_complete_segment(request):
#    template = 'admin/setup-complete.html'
#    context = {}
#    ad_arr = []
#    co, ugs, context = check_company(request, context)
#    cu_id = request.session.get('cu_id', None)
#    if not cu_id:
#        cu_id = request.GET.get('cu_id', None)
#    if not request.user.is_superuser:
#        cu_id = request.user.userprofile.company.number
#    if cu_id:
#        request.session['cu_id'] = cu_id

#    co = Company().get_company(cu_id, 'number')
#    domain = Domain.objects.filter(company=co).first()
#    ad_id = request.GET.get('ad_ids', None)
#    asset_id = request.GET.get('asset_id', None)
#    ad = Ad.objects.filter(id=int(ad_id)).first()
#    asset = Asset.objects.filter(id=int(asset_id)).first()
#    context['ad'] = ad
#    context['asset'] = asset

#    redirect_url = get_base_url(domain, settings.ENV)
#    if not ad.pages:
#        redirect_url += '?ad_ids=%s&segments=%s&api=%s'%(ad_id, asset.demographics, settings.ENV)
#    elif len(ad.pages.split(',')) >= 1:
#        param = ad.pages.split(',')[0]
#        redirect_url += '%s?ad_ids=%s&segments=%s&api=%s'%(param, ad_id, asset.demographics, settings.ENV)
#    if ad.keyword_group:
#        redirect_url += '&products_recommended=' + ad.keyword_group.keyword
#    context['redirect_url'] = redirect_url

#    return render(request, template, context)

#def get_order_id(gs_ids_orders, search_index):
#    lg.info(gs_ids_orders)
#    for i in gs_ids_orders:
#        if i[1] == search_index:
#            temp_id = i[0]
#            break
#    return temp_id

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def update_products_order_ajax(request):
#    status = 0
#    oldIndex = int(request.GET['oldIndex']) if 'oldIndex' in request.GET else None
#    newIndex = int(request.GET['newIndex'])  if 'newIndex' in request.GET else None
#    board_title = request.GET['board_title']  if 'board_title' in request.GET else None

#    cu_id = request.GET.get('cu_id')
#    if not request.user.is_superuser:
#        cu_id = request.user.userprofile.company.number
#    co = Company().get_company(cu_id, 'number')
#    print(oldIndex, newIndex, board_title, cu_id)
#    # if board_title == "default":
#    oldIndex = oldIndex + 1
#    newIndex = newIndex + 1
    
#    # increase old and new indexes by 1 because setting_order of "default" setting_type starts from 1 but not from 0 (other setting_type's order starts from 0). and in js, indexes starts from 0.
#    gs_ids_orders = list(GlobalSetting.objects.filter(company=co, setting_name=board_title).values_list('id', 'setting_order').order_by('setting_order'))
#    #lg.info(('init', gs_ids_orders))
#    oldIndexId = get_order_id(gs_ids_orders, oldIndex)
#    if oldIndex < newIndex:
#        for i in reversed(range(oldIndex+1, newIndex+1)):
#            #lg.info(('old<new', gs_ids_orders))
#            temp_id = get_order_id(gs_ids_orders, i)
#            q=GlobalSetting.objects.get(id=temp_id)
#            q.setting_order=i-1
#            q.save()

#        # update old index with new index
#        q_update_old_ind = GlobalSetting.objects.get(id=oldIndexId)
#        q_update_old_ind.setting_order = newIndex
#        q_update_old_ind.save()
#        status = 1
#    elif newIndex < oldIndex:
#        for i in range(newIndex, oldIndex):
#            #lg.info(('new<old', gs_ids_orders))
#            temp_id = get_order_id(gs_ids_orders, i)
#            q = GlobalSetting.objects.get(id=temp_id)
#            q.setting_order=i+1
#            q.save()
#        # update old index with new index
#        q_update_old_ind = GlobalSetting.objects.get(id=oldIndexId)
#        q_update_old_ind.setting_order=newIndex
#        q_update_old_ind.save()
#        status = 1    
#    return JsonResponse({'status':status})


#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def products_list(request, product_id=None):
#    # del request.session['cu_id']
#    context = {}
#    context['template'] = 'admin/products.html'
#    gs_data = []
#    cu_id = request.GET.get('cu_id')
#    co, ugs, context = check_company(request, context)
#    # if finalytics emp exists but he didnt select any company yet.
#    # if context['is_fin_employee'] and not context['cu_id']:
#    #     return redirect(reverse('choose-company'))

#    # if not cu_id and not request.user.is_superuser:
#    #     cu_id = co.number
#    if context['cu_id'] and not context['cu_id'] == 'all':
#        temp_list = []
#        #co = Company().get_company(cu_id, 'number')

#        gs = GlobalSetting.objects.filter(company=co)
#        setting_list = ['default', 'default.priority.firsttime', 'default.priority.nonmember', 'default.priority.member']
#        setting_labels = ['Default', 'First-time Visitors', 'Returning Prospects', 'Members']
#        if product_id:
#            del_filter = GlobalSetting.objects.filter(id=product_id)
#            deleted_setting_value = del_filter.first().setting_value
#            deleted_setting_name = del_filter.first().setting_name
#            deleted_setting_order = del_filter.first().setting_order
#            gs_count = gs.filter(setting_category="products", setting_name=deleted_setting_name).count()
            
            
#            if not deleted_setting_order == gs_count:
#                initial_count = deleted_setting_order+1
#                for i in range(initial_count, gs_count+1):
#                    gs.filter(setting_category="products", setting_name=deleted_setting_name, setting_order=i).update(setting_order=i-1)
#            del_filter.delete()
#            for ind, i in enumerate(setting_list):
#                if i == deleted_setting_name:
#                    deleted_setting_label = setting_labels[ind]
#                    break
#            messages.success(request, '<span style="color:#000;">'+deleted_setting_value+'</span> successfully removed from <span style="color:#000;">'+deleted_setting_label+'</span> priority list.')
#            return redirect(reverse('products_list')+'?cu_id='+cu_id)

#        if request.method == 'POST':
#            selected_product = request.POST['selected']
#            selected_setting_name = request.POST['setting_name']
#            selected_setting_count = gs.filter(setting_category="products", setting_name=selected_setting_name).count()
#            q = GlobalSetting(company=co, setting_category="products", setting_name=selected_setting_name, setting_value=selected_product, setting_order=selected_setting_count+1)
#            q.save()
#            for ind, i in enumerate(setting_list):
#                if i == selected_setting_name:
#                    seleted_setting_label = setting_labels[ind]
#                    break            
#            messages.success(request, '<span style="color:#000;">'+selected_product+'</span> successfully added to <span style="color:#000;">'+seleted_setting_label+'</span> priority list.')
#            return redirect(reverse('products_list')+'?cu_id='+cu_id)
        
#        setting_names = list(gs.filter(company=co, setting_category='products', setting_name__in=setting_list).values_list('setting_name', flat=True).distinct())

#        # order setting names
#        for i in setting_list:
#            if i in setting_names:
#                temp_list.append(i)
#        setting_names = temp_list
        
#        products = GlobalSetting().get_settings(co, setting_category='products', order_by=['setting_order', 'setting_name'])
#        for i,setting_name in enumerate(setting_names):
#            temp_products = products.filter(setting_name=setting_name)
#            board_label = setting_labels[i]
#            board_title = setting_list[i]
#            gs_data.append({'board_label': board_label, 'board_title': board_title, 'products': temp_products})

#        kg_list = list(KeywordGroup.objects.filter(is_core_product=True, is_active=True).values_list('keyword', flat=True))
#        context['kg_list'] = json.dumps(kg_list)
#        # context['cu_id'] = cu_id
#    # elif not cu_id:
#        # if request.user.is_superuser:
#        #     companies = Company().get_subscribers()
#        #     context['companies'] = companies
#        # return redirect(reverse('products_list')+'?cu_id='+context['cu_id'])
    
#    context['gs_data'] = gs_data
#    #p = cache.get('PCONFIG')
#    #p = p['vys']['products']
#    #context['pconfig'] = PCONFIG['vys']['products']['probabilities']['default']
#    return render(request, context['template'], context)


#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def segments_list(request, segment_id=None):
#    # del request.session['cu_id']
#    context = {}
#    context['template'] = 'admin/segments-list.html'
#    gs_data = []
#    cu_id = request.GET.get('cu_id')
#    co, ugs, context = check_company(request, context)
#    # if finalytics emp exists but he didnt select any company yet.

#    # if context['is_fin_employee'] and not context['cu_id']:
#    #     return redirect(reverse('choose-company'))
        
#    # if not cu_id and not request.user.is_superuser:
#    #     cu_id = co.number

#    if context['cu_id'] and not context['cu_id'] == 'all':
#        #co = Company().get_company(cu_id, 'number')
#        gs = GlobalSetting.objects.filter(company=co)
#        setting_list = ['default']
#        setting_labels = ['Segments']

#        # deletion of segment
#        if segment_id:
#            del_filter = GlobalSetting.objects.filter(id=segment_id)
#            deleted_setting_value = del_filter.first().setting_value
#            deleted_setting_name = del_filter.first().setting_name
#            deleted_setting_order = del_filter.first().setting_order
#            gs_count = gs.filter(setting_subcategory="segments", setting_name=deleted_setting_name).count()
            
#            # if order and count are equal, that means it is the last id of gs, so, it simply needs to be deleted otherwise we need to update the orders of rest of them.
#            if not deleted_setting_order == gs_count:
#                initial_count = deleted_setting_order+1
#                for i in range(initial_count, gs_count+1):
#                    gs.filter(setting_subcategory="segments", setting_name=deleted_setting_name, setting_order=i).update(setting_order=i-1)
#            del_filter.delete()
#            for ind, i in enumerate(setting_list):
#                if i == deleted_setting_name:
#                    deleted_setting_label = setting_labels[ind]
#                    break
#            messages.success(request, '<span style="color:#000;">'+deleted_setting_value+'</span> successfully removed from <span style="color:#000;">'+deleted_setting_label+'</span> priority list.')
#            return redirect(reverse('z-segments')+'?cu_id='+cu_id)

#        if request.method == 'POST':
#            selected_segment = request.POST['selected']
#            selected_setting_name = request.POST['setting_name']
#            selected_setting_count = gs.filter(setting_subcategory="segments", setting_name=selected_setting_name).count()
#            q = GlobalSetting(company=co, setting_subcategory="segments", setting_name=selected_setting_name, setting_value=selected_segment, setting_order=selected_setting_count+1)
#            q.save()
#            for ind, i in enumerate(setting_list):
#                if i == selected_setting_name:
#                    seleted_setting_label = setting_labels[ind]
#                    break            
#            messages.success(request, '<span style="color:#000;">'+selected_segment+'</span> successfully added to <span style="color:#000;">'+seleted_setting_label+'</span> priority list.')
#            return redirect(reverse('z-segments')+'?cu_id='+cu_id)

#        # setting_names = list(gs.filter(company=co, setting_subcategory='segments', setting_name__in=setting_list).values_list('setting_name', flat=True).distinct())        
#        segments = GlobalSetting().get_settings(co, setting_subcategory='segments', order_by=['setting_order', 'setting_name'])
#        # for i,setting_name in enumerate(setting_names):
#        for i,setting_name in enumerate(setting_list):
#            temp_segments = segments.filter(setting_name=setting_name)
#            board_label = setting_labels[i]
#            board_title = setting_list[i]
#        gs_data.append({'board_label': board_label, 'board_title': board_title, 'segments': temp_segments})
#        # context['cu_id'] = cu_id

#        # Suggested Segments
#        kg = list(KeywordGroup.objects.filter(category='segment', is_active=True).values_list('keyword', flat=True))
#        temp_kg = []
#        temp_segments_values = []
#        for k in gs_data:
#            if k['board_title'] == "default":
#                temp_segments_values = list(temp_segments.values_list('setting_value', flat=True))
#                break
#        for i in kg:
#            if i not in temp_segments_values:
#                temp_kg.append({'setting_value': i})

#        # context['cu_id'] = cu_id
#        gs_data.append({'board_label': 'Suggested Segments', 'board_title': 'suggested_segments', 'segments': temp_kg})
#        context['gs_data'] = gs_data
#    # elif not cu_id:
#        # if request.user.is_superuser:
#        # request.session['request_referrer'] = request.path
#        # return redirect(reverse('segments')+'?cu_id='+context['cu_id'])
    

#    return render(request, context['template'], context)

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def update_segments_order_ajax(request):
#    status = 0
#    new_segment_id = None
#    oldIndex = int(request.GET['oldIndex']) if 'oldIndex' in request.GET else None
#    newIndex = int(request.GET['newIndex'])  if 'newIndex' in request.GET else None
#    board_title = request.GET['board_title']  if 'board_title' in request.GET else None
#    dragging_type = request.GET['dragging_type']  if 'dragging_type' in request.GET else None
#    segment_name = request.GET['segment_name']  if 'segment_name' in request.GET else None

#    cu_id = request.GET.get('cu_id')
#    if not request.user.is_superuser:
#        cu_id = request.user.userprofile.company.number
#    co = Company().get_company(cu_id, 'number')
#    print(oldIndex, newIndex, board_title, cu_id)

#    gs_ids_orders = list(GlobalSetting.objects.filter(company=co,setting_subcategory="segments", setting_name=board_title).values_list('id', 'setting_order').order_by('setting_order'))
#    oldIndex = oldIndex + 1
#    newIndex = newIndex + 1
#    if dragging_type == "vertical":
#        oldIndexId = get_order_id(gs_ids_orders, oldIndex)
#        if oldIndex < newIndex:
#            for i in reversed(range(oldIndex+1, newIndex+1)):
#                temp_id = get_order_id(gs_ids_orders, i)
#                q=GlobalSetting.objects.get(id=temp_id)
#                q.setting_order=i-1
#                q.save()

#            # # update old index with new index
#            # q_update_old_ind = GlobalSetting.objects.get(id=oldIndexId)
#            # q_update_old_ind.setting_order = newIndex
#            # q_update_old_ind.save()
#            # status = 1
#        elif newIndex < oldIndex:
#            for i in range(newIndex, oldIndex):
#                temp_id = get_order_id(gs_ids_orders, i)
#                q = GlobalSetting.objects.get(id=temp_id)
#                q.setting_order=i+1
#                q.save()
#        # update old index with new index
#        q_update_old_ind = GlobalSetting.objects.get(id=oldIndexId)
#        q_update_old_ind.setting_order=newIndex
#        q_update_old_ind.save()
#        status = 1
#    elif dragging_type == "right_to_left":
#        last_segment_order = GlobalSetting.objects.filter(company=co,setting_subcategory="segments", setting_name=board_title).count()
#        for i in range(newIndex, last_segment_order+1):
#            temp_id = get_order_id(gs_ids_orders, i)
#            q = GlobalSetting.objects.get(id=temp_id)
#            q.setting_order=i+1
#            q.save()
#        q = GlobalSetting(company=co,setting_subcategory="segments", setting_name=board_title, setting_value=segment_name, setting_order=newIndex)
#        q.save()
#        new_segment_id = q.id
#        status = 1

#    elif dragging_type == "left_to_right":
#        oldIndexId = get_order_id(gs_ids_orders, oldIndex)
#        last_segment_order = GlobalSetting.objects.filter(company=co,setting_subcategory="segments", setting_name=board_title).count()        
#        for i in range(oldIndex+1, last_segment_order+1):
#            temp_id = get_order_id(gs_ids_orders, i)
#            q = GlobalSetting.objects.get(id=temp_id)
#            q.setting_order=i-1
#            q.save()
#        GlobalSetting.objects.filter(id=oldIndexId).delete()
#        status = 1
#    return JsonResponse({'status':status, 'new_segment_id': new_segment_id})

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#@permission_required(['app.add_keywordgroup', 'app.view_keywordgroup', 'app.delete_keywordgroup'], login_url=no_access_url)
#def keywords_list(request):
#    template = 'admin/keywords-list.html'
#    context = {}
#    co, ugs, context = check_company(request, context)
#    # if finalytics emp exists but he didnt select any company yet.
#    # if context['is_fin_employee'] and not context['cu_id']:
#    #     return redirect(reverse('choose-company'))
#    kgs = KeywordGroup.objects.all().order_by('-timestamp_modified')
#    context['kgs'] = kgs
#    return render(request, template, context)

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def revenue_list(request):
#    template = 'admin/revenue-list.html'
#    context = {}
#    co, ugs, context = check_company(request, context)
#    q = RevenueKPI.objects.all().order_by('-timestamp_modified')
#    print('all', q.count())
#    context['revenue_list'] = q
#    return render(request, template, context)

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def rate_list(request):
#    template = 'admin/rate-list.html'
#    context = {}
#    co, ugs, context = check_company(request, context)
#    q = Rate.objects.all().order_by('-timestamp_modified')
#    context['rate_list'] = q
#    return render(request, template, context)

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def offer_list(request):
#    template = 'admin/offer-list.html'
#    context = {}
#    co, ugs, context = check_company(request, context)
#    q = Offer.objects.all().order_by('-timestamp_modified')
#    context['offer_list'] = q
#    return render(request, template, context)

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def faqquestion_list(request):
#    template = 'admin/faq-question-list.html'
#    context = {}
#    co, ugs, context = check_company(request, context)
#    q = FAQQuestion.objects.all().order_by('-timestamp_modified')
#    context['faqquestion_list'] = q
#    return render(request, template, context)

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def delete_model_val(request):
#    import app
#    m_name = request.GET.get('m_name')
#    m_id = request.GET.get('m_id')
#    m_path = request.GET.get('m_path')
#    model = getattr(app.models, m_name)
#    # model.objects.filter(id=m_id).delete()
#    model.objects.filter(id=m_id)
#    return redirect(m_path)

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
def generate_copy(request, ai_type='chat', stage='copy'):
    from openai_tools import bulk_create, create
    template = 'admin/generate-copy.html'
    context = {}
    kwargs = {}
    suggestions = {}
    responses = []
    n = 1
    #co, ugs, context = check_company(request, context)
    instructions = segments = suggestion = None
    s = 'create ad copy for a %s'
    #if ai_type == 'start':
    #    ai_type = 'chat'
    context['ai_type'] = ai_type
    context['stage'] = stage
    if request.method == "POST":
        flow = int(request.POST.get('flow', 0))
        if flow != 1:
            if stage != 'prod':
                n = int(request.POST.get('choice', 3))
            else:
                n = int(request.POST.get('choice', 1))
        else:
            n = int(request.POST.get('choice', 1))
        temperature = float(request.POST.get('temperature', 0.7))
        top_p = float(request.POST.get('top_p', 0.9))
        max_tokens = int(request.POST.get('max_tokens', 75))
        suggestion = request.POST.get('suggestion', None)
        context['flow'] = flow
        context['temperature'] = temperature
        context['top_p'] = top_p
        context['max_tokens'] = max_tokens
        lg.info(('flow, choices, temperature, top_p, max_tokens', flow, n, temperature, top_p, max_tokens))
        lg.info(('suggestion', suggestion))
        #if suggestion:
        #    s = suggestion
        #    stage = 'segment'
        if stage == 'prod':
            n = 2
        #if ai_type == 'edits' and stage != 'segment':
        #    n = 1
        prod = request.POST.get('prod', None)
        segs = request.POST.get('segments', None)
        lg.info(('prod', prod))
        lg.info((ai_type, stage, n))
        lg.info(('segs', segs))
        if flow != 1:
            if stage != 'copy':
                if not segs:
                    segs = "retiree, student, family"
            else:
                segs = ""
        if segs:
            segments = sorted([seg.strip() for seg in segs.split(',')]) #, 'teenager', 'retiree', 'educator']

        lg.info(('segments: ', segments))
        lg.info(s)
        if flow != 1:
            if ai_type == 'chat' and stage == 'segment':
                lg.info(('chat segments', segments))
                # s = 'rewrite the following ad copy text for a %s: %s'
                s = 'rewrite the following %s ad copy text for a %s'
                #n = len(segments)
                # n = 1
                prompts = [(s)%(seg, suggestion) for seg in segments]
            elif ai_type == 'chat' and stage != 'prod':
                lg.info(('edits segments', segments))
                # s = 'create ad copy for a %s for %s'
                # #n = len(segments)
                # prompts = [(s)%(prod, seg) for seg in segments]
                s = 'create ad copy for a %s'
                #n = len(segments)
                prompts = [(s)%(prod)]
            elif ai_type == 'edits' and stage == 'segment':
                prompt = suggestion
                # instructions = [('rewrite the following ad copy text for a %s')%(seg) for seg in segments]
                instructions = [('rewrite the following %s ad copy for a %s')%(prod, seg) for seg in segments]
            else:
                prompts = [(s)%(prod)]
        else:
            if ai_type == 'chat' and stage == 'segment':
                lg.info(('chat segments', segments))
                # s = 'rewrite the following ad copy text for a %s: %s'
                s = 'rewrite the following %s ad copy for a %s '
                #n = len(segments)
                # n = 1
                prompts = [(s)%(seg, suggestion) for seg in segments]
            elif ai_type == 'chat' and stage != 'prod':
                lg.info(('edits segments', segments))
                s = 'create ad copy for a %s for %s'
                # #n = len(segments)
                prompts = [(s)%(prod, seg) for seg in segments]
            elif ai_type == 'edits' and stage == 'segment':
                prompt = suggestion
                # instructions = [('rewrite the following ad copy text for a %s')%(seg) for seg in segments]
                instructions = [('rewrite the following %s ad copy for a %s')%(prod, seg) for seg in segments]
            else:
                prompts = [(s)%(prod)]
        lg.info((prod, segments))
        if flow != 1:
            if ai_type == 'edits' and stage == 'segment':
                for instruction in instructions:
                    kwargs = {'n':n, 'instruction':instruction}
                    lg.info(kwargs)
                    lg.info(('prompt', prompt))
                    responses.append(create(prompt, ai_type, temperature, top_p, max_tokens, kwargs))
            else:
                lg.info((prompts, ai_type, n))
                responses = bulk_create(prompts, ai_type, temperature, top_p, max_tokens, n=n)
        else:
            if ai_type == 'edits':
                for instruction in instructions:
                    kwargs = {'n':n, 'instruction':instruction}
                    lg.info(kwargs)
                    lg.info(('prompt', prompt))
                    responses.append(create(prompt, ai_type, temperature, top_p, max_tokens, kwargs))
            else:
                lg.info((prompts, ai_type, n))
                responses = bulk_create(prompts, ai_type, temperature, top_p, max_tokens, n=n)
        if stage != 'segment':
            context['prompts'] = prompts
        context['product'] = prod
        context['segments'] = segments
        if responses:
            if flow != 1:
                if ai_type == 'completions' and stage != 'prod':
                    for i,r in enumerate(responses):
                        suggestions[segments[i]] = r.choices[0].text.strip()
                elif ai_type == 'edits' and stage == 'segment':
                    lg.info(responses)
                    for j,response in enumerate(responses):
                        for i,r in enumerate(response.choices):
                            if segments[j] in r['text'].strip().lower():
                                suggestions[segments[j]] = remove_cutoff_sentence(r['text'].strip())
                                print("The sentence contains the word")
                            else:
                                print("The sentence does not contain the word", segments, segments[j], suggestions.get(segments[j]))
                                if suggestions.get(segments[j]) == None or suggestions.get(segments[j]) == "":
                                    suggestions[segments[j]] = remove_cutoff_sentence(r['text'].strip())
                    # for i,r in enumerate(responses):
                    #     suggestions[segments[i]] = r.choices[0].text.strip()
                elif ai_type == 'chat':
                    lg.info(responses)
                    if stage in ['segment']:
                        # for i,r in enumerate(responses):
                        #     suggestions[segments[i]] = r.choices[0]['message']['content'].strip()
                        for j,response in enumerate(responses):
                            for i,r in enumerate(response.choices):
                                if segments[j] in r['message']['content'].strip().lower():
                                    suggestions[segments[j]] = remove_cutoff_sentence(r['message']['content'].strip())
                                    print("The sentence contains the word")
                                else:
                                    print("The sentence does not contain the word", suggestions.get(segments[j]))
                                    if suggestions.get(segments[j]) == None or suggestions.get(segments[j]) == "":
                                        suggestions[segments[j]] = remove_cutoff_sentence(r['message']['content'].strip())
                                # suggestions[segments[j]] = r['message']['content'].strip()
                            # suggestions[segments[i]] = r['message']['content'].strip()
                    elif stage in ['copy']:
                        for i,r in enumerate(responses[0].choices):
                            if not segments:
                                suggestions[i] = remove_cutoff_sentence(r['message']['content'].strip())
                            else:
                                suggestions[segments[i]] = remove_cutoff_sentence(r['message']['content'].strip())
                    else:
                        for i,r in enumerate(responses[0].choices):
                            suggestions[i] = remove_cutoff_sentence(r['message']['content'].strip())
                else:
                    response = responses[0]
                    lg.info(response)
                    if response:
                        for i,r in enumerate(response.choices):
                            suggestions[i] =remove_cutoff_sentence(r.text.strip())
            else:
                if ai_type == 'completions' and stage != 'prod':
                    for i,r in enumerate(responses):
                        suggestions[segments[i]] = remove_cutoff_sentence(r.choices[0].text.strip())
                elif ai_type == 'edits':
                    lg.info(responses)
                    for j,response in enumerate(responses):
                        for i,r in enumerate(response.choices):
                            if segments[j] in r['text'].strip().lower():
                                suggestions[segments[j]] = remove_cutoff_sentence(r['text'].strip())
                                print("The sentence contains the word")
                            else:
                                print("The sentence does not contain the word", segments, segments[j], suggestions.get(segments[j]))
                                if suggestions.get(segments[j]) == None or suggestions.get(segments[j]) == "":
                                    suggestions[segments[j]] = remove_cutoff_sentence(r['text'].strip())
                    # for i,r in enumerate(responses):
                    #     suggestions[segments[i]] = r.choices[0].text.strip()
                elif ai_type == 'chat':
                    for j,response in enumerate(responses):
                        for i,r in enumerate(response.choices):
                            if segments[j] in r['message']['content'].strip().lower():
                                suggestions[segments[j]] = remove_cutoff_sentence(r['message']['content'].strip())
                                print("The sentence contains the word")
                            else:
                                print("The sentence does not contain the word", suggestions.get(segments[j]))
                                if suggestions.get(segments[j]) == None or suggestions.get(segments[j]) == "":
                                    suggestions[segments[j]] = remove_cutoff_sentence(r['message']['content'].strip())
                else:
                    response = responses[0]
                    lg.info(response)
                    if response:
                        for i,r in enumerate(response.choices):
                            suggestions[i] = remove_cutoff_sentence(r.text.strip())
        else:
            lg.info('No responses')
        context['suggestions'] = suggestions
    context['suggestion'] = suggestion
    #lg.info(context)

    return render(request, template, context)

def generate_copy_history(request):
    lg.info(('generate_copy_history: '))
    template = 'admin/generate-copy-history.html'
    suggestions = {}
    context = {}
    if request.method == "POST":
        history = request.POST.get('history', None)
        data = json.loads(history)
        lg.info(('history: ', data))
        context['ai_type'] = data['ai_type']
        context['product'] = data['product']
        context['segments'] = data['segments']
        segments = data['segments']
        if len(segments) == 0:
            suggestions = data['suggestions']
        else:
            for i,r in enumerate(data['suggestions']):
                suggestions[segments[i]] = r
        context['suggestions'] = suggestions
        context['temperature'] = data['temperature']
        context['top_p'] = data['top_p']
        context['max_tokens'] = data['max_tokens']
    return render(request, template, context)
    
def generate_copy_list_data(request):
    if request.method == 'POST':
        product = request.POST.get('product', None)
        segs = request.POST.get('segments', None)
        suggestions = request.POST.get('suggestions', None)
        segments = []
        if segs:
            segments = sorted([seg.strip() for seg in segs.split(',')]) #, 'teenager', 'retiree', 'educator']
        data = {
            'product': product,
            'segments': segments,
            'suggestions': suggestions
        }
        json_data = json.dumps(data)
        lg.info(('product: ', product))
        lg.info(('segments: ', segments))
        lg.info(('suggestions: ', suggestions))
        return JsonResponse({'data': data})
    
def remove_cutoff_sentence(text):
    # Define regular expression pattern to split string into sentences
    pattern = r'(?<=[^A-Z].[.?]) +(?=[A-Z])'

    # Split text into sentences
    sentences = re.split(pattern, text)

    # Check if the last sentence is being cutoff
    last_sentence = sentences[-1].strip()
    if last_sentence[-1] not in ['.', '!', '?']:
        # Remove last sentence if it is being cutoff
        sentences = sentences[:-1]

    # Rejoin the remaining sentences into a single string
    new_text = ' '.join(sentences)

    return new_text
#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#@permission_required(['app.add_adtemplate', 'app.view_adtemplate', 'app.delete_adtemplate'], login_url=no_access_url)
#def content_module_templates(request):
#    from django.db.models import Q
#    template = 'admin/content-module-templates.html'
#    context = {}
#    co, ugs, context = check_company(request, context)
#    print('ugs', ugs)
#    if request.user.groups.filter(Q(name="personalization_staff") | Q(name="personalization_admin")):
#        adtemplates = AdTemplate.objects.filter(company=request.user.userprofile.company).order_by('-timestamp_modified')
#    else:
#        adtemplates = AdTemplate.objects.all().order_by('-timestamp_modified')
#    context['adtemplates'] = adtemplates
#    return render(request, template, context)

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def copy_content_modules(request):
#    template = 'admin/copy-content-modules.html'
#    context = {}
#    adcopies = AdCopy.objects.all().order_by('-timestamp_modified')
#    context['adcopies'] = adcopies
#    return render(request, template, context)

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#@permission_required(['auth.add_user', 'auth.view_user', 'auth.delete_user'], login_url=no_access_url)
#def users_listing(request):
#    from django.contrib.auth.models import User
#    users = []
#    template = 'admin/users-list.html'
#    context = {}
#    co, ugs, context = check_company(request, context)
#    if request.user.groups.filter(name="personalization_admin"):
#        c = request.user.userprofile.company
#        users = c.userprofile_set.all().order_by('user__date_joined')
#    else:
#        users = UserProfile.objects.all().order_by('user__date_joined')  
#    context['users']= users
#    return render(request, template, context)


#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def campaign_url(request):
#    context = {}
#    co, ugs, context = check_company(request, context)
#    utm_term = request.GET['utm_term'] if 'utm_term' in request.GET else None
#    context = {
#        'utm_term': "&utm_term=%s"%utm_term
#    }
#    return render(request, 'admin/campaign-url.html', context)

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def campaign_content_modules(request):
#    ad_images = []
#    context = {}
#    co, ugs, context = check_company(request, context)
#    utm_term = request.GET['utm_term'] if 'utm_term' in request.GET else None
#    if request.user.is_superuser:
#        ads = Ad.objects.all().order_by('-timestamp_created')
#    else:
#        ads = Ad.objects.filter(company=request.user.userprofile.company).order_by('-timestamp_created')
#    for ad in ads:
#        temp_ad_list = []
#        temp_ad_list.append(ad)
#        ad_images.append(get_ad_first_image(ad.company, temp_ad_list))

#    context = {
#        'ads': zip(ad_images, ads),
#        'utm_term': utm_term if utm_term else None
#    }
#    return render(request, 'admin/campaign-content-modules.html', context)

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def campaign_type(request):
#    template = "admin/campaign-type.html"
#    context = {}
#    products = []
#    segments = []
#    services = []
#    locations = []
#    co, ugs, context = check_company(request, context)
#    cu_id = request.GET.get('cu_id')
#    if not request.user.is_superuser:
#        cu_id = request.user.userprofile.company.number
#    if cu_id:      
#        co = Company().get_company(cu_id, 'number')  
#        if request.method == "POST":
#            product = request.POST['product'] if 'product' in request.POST else None
#            service = request.POST['service'] if 'service' in request.POST else None
#            location = request.POST['location'] if 'location' in request.POST else None
#            segment = request.POST['segment'] if 'segment' in request.POST else None
#            utm_term = "utm_term="
#            if product or service:
#                if product:
#                    utm_term += "p__%s,"%product
#                elif service:
#                    utm_term += "s__%s,"%service
#            if location:
#                utm_term += "loc__%s,"%location
#            if segment:
#                utm_term += "seg__%s"%segment
            
#            return redirect(reverse('campaign_content_modules')+"?"+utm_term)

#            # if product and not service and not location:
#            #     save_category(co, 'products', product, segment, single_item=True)
#            # elif not product and service and not location:
#            #     save_category(co, 'services', service, segment, single_item=True)
#            # elif not product and not service and location:
#            #     save_category(co, 'locations', location, segment, single_item=True)
#            # elif product or service and location:
#            #     setting_category = None
#            #     if product:
#            #         temp_type = "products"
#            #         temp_val = product
#            #     else:
#            #         temp_type = "services"
#            #         temp_val = service
#            #     save_category(co, temp_type, temp_val, segment, single_item=False)
            
#        data = KeywordGroup.objects.filter(is_active=True, is_biz=False).exclude(category=None).order_by('keyword')
#        products = data.filter(category='product')
#        segments = data.filter(category='segment')
#        services = data.filter(category='service')
#        locations = data.filter(category='location')
        
#        context['products'] = products
#        context['segments'] = segments
#        context['services'] = services
#        context['locations'] = locations
#    elif not cu_id:
#        if request.user.is_superuser:
#            companies = Company().get_subscribers()
#            context['companies'] = companies        
#    return render(request, template, context)    



#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def update_content_module(request):
#    ad_id = int(request.GET.get('ad_id')) if 'ad_id' in request.GET else None
#    is_active_chk = request.GET.get('is_active_chk') if 'is_active_chk' in request.GET else None
#    if not ad_id or not is_active_chk:
#        status = 0
#        message='Data input error'
#    else:
#        is_active = True
#        if is_active_chk == "false":
#            is_active = False
#        Ad.objects.filter(id=ad_id).update(is_active=is_active)
#        status = 1
#        message='Ad Status Updated Successfully.'        
        
#    return JsonResponse({'status':status, 'message': message})

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def update_scenario(request):
#    campaign_val = int(request.GET.get('campaign_val')) if 'campaign_val' in request.GET else None
#    is_active_chk = request.GET.get('is_active_chk') if 'is_active_chk' in request.GET else None
#    if not campaign_val or not is_active_chk:
#        status = 0
#        message='Data input error'
#    else:
#        is_active = True
#        if is_active_chk == "false":
#            is_active = False
#        Campaign.objects.filter(id=campaign_val).update(is_active=is_active)
#        status = 1
#        message='Campaign Status Updated Successfully.'        
        
#    return JsonResponse({'status':status, 'message': message})
    
#def check_img_exists(company, img_url):
#    from pmodels import check_url_start
#    if check_url_start(img_url):
#        if img_url.startswith('/'):
#            img_url = img_url[1:]
#        temp_img_url = os.path.join(settings.MEDIA_ROOT, company.code, img_url)
#        if os.path.exists(temp_img_url):
#            img_url = ('%s%s/%s')%(settings.MEDIA_URL, company.code, img_url)
#        else:
#            base_url = company.get_platform_mode(env=settings.ENV, next_env=True)
#            if base_url:
#                if check_url_start(base_url):
#                    #url does NOT start with http or //
#                    img_url = 'https://' + base_url + '/' + img_url
#                else:
#                    img_url = base_url + '/' + img_url
#    return img_url

#def get_ad_first_image(company, temp_ad_list):
#    from pmodels import get_ad_images, get_scrape_demo_url
#    ad_image = '/static/app/images/no-image.png'
#    images = get_ad_images(company, temp_ad_list, exclude_assets=True)
#    if images:
#        ad_image = check_img_exists(company, images[0])
#    return ad_image

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def all_content_modules(request):
#    ad_images = []
#    context = {}
#    context['template'] = 'admin/content-modules.html'
#    co, ugs, context = check_company(request, context)
#    if context['cu_id'] or context['cu_id'] == '':
#        if context['cu_id'] == 'all' or context['cu_id'] == '':
#            context['template'] = 'admin/content-modules.html'
#            ads = Ad.objects.all().order_by('-timestamp_created')
#        else:
#            ads = Ad.objects.filter(company=co).order_by('-timestamp_created')
#        for ad in ads:
#            ad_images.append(get_ad_first_image(ad.company, [ad]))

#        context['ads'] = zip(ad_images, ads)
#    return render(request, context['template'], context)    

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def content_modules(request, campaign_id):
#    ad_images = []
#    context = {}
#    co, ugs, context = check_company(request, context)
#    q=Campaign.objects.get(id=campaign_id)
#    ads = q.ad_set.all()
#    for ad in ads:
#        temp_ad_list = []
#        temp_ad_list.append(ad)
#        ad_images.append(get_ad_first_image(q.company, temp_ad_list))

#    context = {
#        'ads': zip(ad_images, ads)
#    }
#    return render(request, 'admin/content-modules.html', context)    

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def scenarios(request):
#    template = 'admin/scenarios.html'
#    context = {}
#    from pmodels import get_ad_images, get_scrape_demo_url, check_url_start
#    from os import path
#    images_list = []
#    co, ugs, context = check_company(request, context)
#    if request.user.is_superuser:
#        # campaigns_list = Campaign.objects.values('id', 'name', 'is_active', 'company__name').order_by('-timestamp_created')
#        campaigns = Campaign.objects.all().order_by('-timestamp_created')
#    else:
#        campaigns = Campaign.objects.filter(company=request.user.userprofile.company).order_by('-timestamp_created')

#    for campaign in campaigns:
#        ads = campaign.ad_set.all()
#        if campaign.id != 4:
#            images = get_ad_images(campaign.company, ads)

#        if images:
#            if not check_url_start(images[0]):
#                images_list.append(images[0])
#            else:
#                img_url = get_scrape_demo_url(campaign.company, images[0])
#                temp_img_url = "%s/app%s"%(settings.BASE_DIR, img_url)
#                images_list.append(img_url if path.exists(temp_img_url) else '/static/app/images/no-image.png')
#        else:
#            images_list.append('/static/app/images/no-image.png')

#    context = {
#        'scenarios_list': zip(images_list, campaigns),
#        'images_list': images_list
#    }
#    return render(request, template, context)




#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def campaigns_list(request):
#    # del request.session['cu_id']
#    context = {}
#    campaigns_list = []
#    context['template'] =  'admin/campaigns_list.html'
#    co, ugs, context = check_company(request, context)
#    # if context['is_fin_employee'] and not context['cu_id']:
#    #     return redirect(reverse('choose-company'))

#    if context['cu_id'] and not context['cu_id'] == 'all':
        
#        campaigns_list = Campaign.objects.filter(company=co, campaign_type="ab").values('id', 'name', 'is_active', 'company__name').order_by('-is_active', '-timestamp_modified')

#    # if request.user.is_superuser:
#    #     campaigns_list = Campaign.objects.filter(campaign_type="ab").values('id', 'name', 'is_active', 'company__name').order_by('-is_active', '-timestamp_modified')
#    # else:
#    #     campaigns_list = Campaign.objects.filter(company=request.user.userprofile.company, campaign_type="ab").values('id', 'name', 'is_active', 'company__name').order_by('-is_active', '-timestamp_modified')
    
#    context['campaigns_list'] = campaigns_list
#    return render(request, context['template'], context)


#def CI(imp, cl, typ):
#    alpha = 100-typ
#    alpha = alpha/100
#    beta = 1 - (alpha/2)
#    ctr = cl/imp
#    temp = norm.ppf(beta)*math.sqrt( (ctr)*(1-ctr)/imp )
#    lwr = (ctr - temp) * 100
#    upr = (ctr + temp) * 100
#    return [round(lwr,2),round(upr,2)]

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def campaign_report(request, campaign_id):
#    template = 'admin/campaign-report.html'
#    result = {}
#    context = {}
#    campaign_name = ''
#    days_running = 0
#    z = {"95%": 1.96, 
#         "90%": 1.65, 
#         "99%": 2.58}

#    co, ugs, context = check_company(request, context)
#    tracking_records = Tracking.objects.values('id', 'company_id', 'ad__name', 'ad_id', 'campaign_id', 'days_running', 'impressions', 'clicks').filter(campaign_id=campaign_id)
#    campaign = Campaign.objects.filter(id=campaign_id).first()
#    if campaign:
#        campaign_name = campaign.name

#    # if no tracking records exist for the corresponding campaign
#    if not tracking_records:
#        context = {
#            'result': result, 
#            'campaign_id': campaign_id, 
#            'campaign_name': campaign_name, 
#            'ads_count': tracking_records.count(), 
#            'message': 'There are no analytics data for this campaign, yet.'
#            }
#    else:
#        days_running_tracks = tracking_records.first()
#        if days_running_tracks:
#            days_running = days_running_tracks['days_running']
#        # if only one ad tracking record exists for the corresponding campaign rather than 2
#        ads_count = Tracking.objects.filter(campaign_id=campaign_id).values('ad_id').distinct().count()
#        if ads_count == 1:
#            context = {
#                'campaign_name': campaign_name,
#                'days_running': 0,
#                'improvement': 0,
#                'result': result,
#                'total_visitors': 0,
#                'ads_count': ads_count
#            }
#        else:
#            df = pd.DataFrame(tracking_records)
#            camp = df.groupby(['campaign_id','ad_id', 'ad__name'])[['impressions','clicks']].sum()
#            camp = camp.reset_index()
#            check = camp['clicks'] > camp['impressions'] 
#            print("camp['clicks']", camp['clicks'])
#            print("camp['impressions']", camp['impressions'])
#            if True in list(check): 
#                print("clicks cannot be greater than impressions for an ad") 

#            camp['cr'] = camp.apply(lambda x: round((x['clicks']/x['impressions']*100),2), axis=1) 
#            camp['confidence_interval_cr'] = camp.apply(lambda x: CI( x['impressions'], x['clicks'], 95 ), axis=1)

#            result = camp.to_dict()
#            # calculate improvement
#            a=0
#            b=0
#            temp = 0
#            if result['cr'][0] > result['cr'][1]:
#                a=result['cr'][0]
#                b=result['cr'][1]
#                temp = 0
#            else:
#                temp = 1
#                a=result['cr'][1]
#                b=result['cr'][0]
    
#            winning_ad = result['ad__name'][temp]
#            improvement = round(((a-b)/b)*100,2)
#            total_visitors = result['impressions'][0] + result['impressions'][1]
#            conf = {}
#            conf[0] = round(result['confidence_interval_cr'][0][1] - result['cr'][0], 1)
#            conf[1] = round(result['confidence_interval_cr'][1][1] - result['cr'][1], 1)
#            context = {
#                'result': result, 
#                'campaign_name': campaign_name, 
#                'days_running': days_running, 
#                'conf': conf,
#                'improvement': improvement, 
#                'winning_ad': winning_ad, 
#                'total_visitors': total_visitors,
#                'ads_count': ads_count
#                }
#    return render(request, template, context)

#class get_image_lists_assets_revised(View):
#    @method_decorator(login_required(login_url=consumer_login_target_url))
#    @method_decorator((user_passes_test(check_perms, login_url=no_access_url)))    
#    @method_decorator(check_cu_user_revised)
#    @method_decorator(check_mfa_setup)
#    def get(self, request, company_code=None, dir_name=None):
#        # del request.session['cu_id']
#        context = {}
#        context['template'] = 'admin/company_image_lists_asset_revised.html'
#        dir_str = ''
#        kwargs = {}
#        assets_count = 0
#        co, ugs, context = check_company(request, context)
#        is_dir_enabled = request.path.endswith('/dir/') or request.path.endswith('/dir')
#        selected_image_width = request.GET.get('image_width', None)
#        asset_companies = Asset.objects.values_list('company', flat=True).exclude(company=None).distinct()
#        scraped_company_list = Company.objects.filter(id__in=asset_companies).order_by('name')

#        context['company_list'] = scraped_company_list
#        context['dir_str'] = dir_str
#        context['is_dir_enabled'] = is_dir_enabled
            

#        co, ugs, context = check_company(request, context)
#        # if finalytics emp exists but he didnt select any company yet.
#        # if context['is_fin_employee'] and not context['cu_id']:
#        #     return redirect(reverse('choose-company'))
#        company_code = co.code

#        if is_dir_enabled:
#            dir_str = 'dir'
#            scraped_company_list = Company.objects.filter(company_type='credit_union').exclude(code=None).exclude(code='').order_by('name')


#        if context['cu_id'] and not context['cu_id'] == 'all' and company_code and not company_code == 'dir':
#            company = co
#            context['selected_company'] = company
#            #if /dir is passed            
#            if is_dir_enabled:
#                lg.info('using get_image_dict aka directory')
#                image_widths = []
#                file_path = os.path.join('static', 'sites', company.code)
#                if company.scrape_demo_base_url:
#                    file_path = os.path.join('app', 'static', 'sites', company.code, company.scrape_demo_base_url)
#                    if settings.ENV_OS == 'linux':
#                        file_path = os.path.join('static', 'sites', company.code, company.scrape_demo_base_url)
#                list_images = traverse_dir(fn='', fp=file_path)
#                image_dict = get_image_dict(list_images)
#                for width in sorted(image_dict, reverse=True):
#                    counter = [len(x) for x in image_dict[width].values()]
#                    image_widths.append([width, sum(counter)])
#            else:
#                lg.info(('using assets table for', co, company_code))
#                image_widths = list(Asset.objects.values_list('width').filter(company__code=company_code).exclude(width=None, height=None).distinct().order_by('-width').annotate(count_images=Count('width')))
#                # image_widths.insert(0,['All', Asset.objects.filter(company__code=company_code).count()])
#                assets_count = Asset.objects.filter(company__code=company_code).exclude(width=None, height=None).count()
#                if image_widths and not selected_image_width:
#                    selected_image_width = image_widths[0][0]



#            if selected_image_width:
#                list_images = []
#                img_dict = {}
                
#                #if image width is None (mostly when image is corrupt or is 0x0)
#                if selected_image_width == '0':
#                    selected_image_width = None
#                if is_dir_enabled and selected_image_width != 0:
#                    #converting recieved image_dict data into list instead of 2d array
#                    for width, width_values in sorted(image_dict.items(), reverse=True):
#                        if int(selected_image_width) == width:
#                            img_dict[width]={}
#                            for height, height_values in sorted(width_values.items(), reverse=True):
#                                img_dict[width][height] = height_values
#                else:
#                    kwargs['company__code'] = company_code
#                    if not selected_image_width == 'all':
#                        kwargs['width'] = selected_image_width

#                    list_images = Asset.objects.values('id', 'short_url', 'width', 'height', 'filename', 'demographics').filter(**kwargs).exclude(width=None, height=None).order_by('-width', '-height')
#                    lg.info(list_images.count())
#                    if selected_image_width == 'all':
#                        lg.info('image_width=all')
#                        for width_value in image_widths:
#                            img_dict[width_value[0]] = {}
#                            temp_data = []
#                            for imgs in list_images:
#                                if imgs['width'] == width_value[0]:
#                                    url = imgs['short_url'].replace('/app/', '/')
#                                    if company.code == 'vys':
#                                        url = '/static/sites/'+ company.code + '/www.stgfinalyticsdemo.com' + imgs['short_url']
#                                    elif company.scrape_demo_base_url and '/static/sites/' not in imgs['short_url']:
#                                        url = '/static/sites/'+ company.code + '/' + company.scrape_demo_base_url + imgs['short_url']
#                                    data = {
#                                        'id':imgs['id'], 
#                                        'url':url,
#                                        'height': imgs['height'],
#                                        'filename': imgs['filename'],
#                                        'demographics': imgs['demographics'],
#                                    }
#                                    temp_data.append(data)
#                            img_dict[width_value[0]] = temp_data
#                        # image_widths.insert(0,['All', Asset.objects.filter(company__code=company_code).count()])
#                    else:

#                        for imgs in list_images:
#                            if imgs['width'] not in img_dict.keys():
#                                img_dict[imgs['width']] = {}
#                            if imgs['height'] not in img_dict[imgs['width']].keys():
#                                img_dict[imgs['width']][imgs['height']] = []
#                            url = imgs['short_url'].replace('/app/', '/')
#                            if company.code == 'vys':
#                                url = '/static/sites/'+ company.code + '/www.stgfinalyticsdemo.com' + imgs['short_url']
#                            elif company.scrape_demo_base_url and '/static/sites/' not in imgs['short_url']:
#                                url = '/static/sites/'+ company.code + '/' + company.scrape_demo_base_url + imgs['short_url']
#                            data = {
#                                'id':imgs['id'], 
#                                'url':url,
#                                'filename': imgs['filename'],
#                                'demographics': imgs['demographics'],
#                            }
#                            img_dict[imgs['width']][imgs['height']].append(data)
#                context['image_data'] = img_dict

#            context['image_widths'] = image_widths
#            context['selected_image_width'] = selected_image_width
#            context['assets_count'] = assets_count
#        #print(context)
#        # elif not company_code:
#            # if request.user.is_superuser:
#            #     companies = Company().get_subscribers()
#            #     context['company_list'] = companies
#            # return redirect(reverse('media-library')+'?cu_id='+context['cu_id'])

#        return render(
#            request,
#            context['template'],
#            context
#        )


#class get_image_lists_assets(View):
#    @method_decorator(login_required(login_url=consumer_login_target_url))
#    @method_decorator((user_passes_test(check_perms, login_url=no_access_url)))
#    @method_decorator(check_cu_user)
#    @method_decorator(check_mfa_setup)
#    def get(self, request, company_code=None, dir_name=None):
#        dir_str = ''
#        is_dir_enabled = request.path.endswith('/dir/') or request.path.endswith('/dir')
#        selected_image_width = request.GET.get('image_width')
#        asset_companies = Asset.objects.values_list('company', flat=True).exclude(company=None).distinct()
#        scraped_company_list = Company.objects.filter(id__in=asset_companies).order_by('name')
#        if is_dir_enabled:
#            print('is_dir_enabled')
#            dir_str = 'dir'
#            scraped_company_list = Company.objects.filter(company_type='credit_union').exclude(code=None).exclude(code='').order_by('name')

#        context = {
#                'company_list':scraped_company_list,
#                'dir_str':dir_str,
#                'is_dir_enabled':is_dir_enabled,
#            }

#        if company_code and not company_code == 'dir':
#            company = Company.objects.filter(code=company_code).first()
#            context['selected_company'] = company
#            #if /dir is passed            
#            if is_dir_enabled:
#                print('using get_image_dict')
#                image_widths = []
#                file_path = os.path.join('static', 'sites', company.code)
#                if company.scrape_demo_base_url:
#                    file_path = os.path.join('app', 'static', 'sites', company.code, company.scrape_demo_base_url)
#                    if settings.ENV_OS == 'linux':
#                        file_path = os.path.join('static', 'sites', company.code, company.scrape_demo_base_url)
#                list_images = traverse_dir(fn='', fp=file_path)
#                image_dict = get_image_dict(list_images)
#                for width in sorted(image_dict, reverse=True):
#                    counter = [len(x) for x in image_dict[width].values()]
#                    image_widths.append([width, sum(counter)])
#            else:
#                image_widths = list(Asset.objects.values_list('width').filter(company__code=company_code).distinct().order_by('-width').annotate(count_images=Count('width')))
            
#            if selected_image_width: 
#                list_images = []
#                img_dict = {}
                
#                #if image width is None (mostly when image is corrupt or is 0x0)
#                if selected_image_width == '0':
#                    selected_image_width = None
#                if is_dir_enabled and selected_image_width != 0:
#                    #converting recieved image_dict data into list instead of 2d array
#                    for width, width_values in sorted(image_dict.items(), reverse=True):
#                        if int(selected_image_width) == width:
#                            img_dict[width]={}
#                            for height, height_values in sorted(width_values.items(), reverse=True):
#                                img_dict[width][height] = height_values
#                else:
#                    list_images = Asset.objects.values('id', 'short_url', 'width', 'height').filter(company__code=company_code, width=selected_image_width).order_by('-width', '-height')
#                    for imgs in list_images:
#                        if imgs['width'] not in img_dict.keys():
#                            img_dict[imgs['width']] = {}
#                        if imgs['height'] not in img_dict[imgs['width']].keys():
#                            img_dict[imgs['width']][imgs['height']] = []
#                        id = company.id
#                        url = imgs['short_url'].replace('/app/', '/')
#                        if company.code == 'vys':
#                            url = '/static/sites/'+ company.code + '/www.stgfinalyticsdemo.com' + imgs['short_url']
#                        elif company.scrape_demo_base_url and '/static/sites/' not in imgs['short_url']:
#                            url = '/static/sites/'+ company.code + '/' + company.scrape_demo_base_url + imgs['short_url']
#                        data = {
#                            'id':imgs['id'],
#                            'url':url,
#                        }
#                        img_dict[imgs['width']][imgs['height']].append(data)
#                context['image_data'] = img_dict

#            context['image_widths'] = image_widths
#            context['selected_image_width'] = selected_image_width
#        #print(context)
#        return render(
#            request,
#            'app/company_image_lists_asset.html',
#            context
#        )


#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def command_manager(request, company_code=None, dir_name=None):
#    template = 'app/command_manager.html'
#    usernames = ['sbarnard@extractable.com', 'jim@webdevelopment.com']
#    command_list = ['testing', 'testp']
#    command = ''
#    context = {'output':'failed'}
#    if not request.user.username in usernames:
#        context['msg'] = 'You are Unauthorized to access this page.'

#    if request.method == 'POST':
#        output = None
#        status = 'error'
#        msg = 'command not found!!!!'
#        command = str(request.POST.get('command'))
#        if command.split()[0] in command_list:
#            try:
#                exec_command = 'python manage.py ' + command
#                output = sp.check_output(exec_command, shell=True)
#                #output = os.popen(exec_command).read()
#                msg = 'command run successfully'
#            except Exception as e:
#                msg = str(e)
#                status = 'exception'
#            if output:
#                #print('len output')
#                #print(len(output))
#                #context['output'] = output
#                output = str(output,'utf8')

#    return render(
#        request,
#        template,
#        locals()
#    )

#@login_required(login_url=consumer_login_target_url)
#@user_passes_test(check_perms_fi, login_url=no_access_url)
#@check_mfa_setup
#def qa(request, company_code=None):
#    template = 'app/qa.html'
#    dir_name = []
#    img_list = {}
#    selected_dir = request.GET.get('selected_dir')
#    list_ext = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
#    company_list = Company.objects.filter(personalization_is_active=True)
#    context = {
#        'company_list':company_list,
#        'template':template,
#    }

#    if company_code:
#        company = Company.objects.get(code=company_code)
#        context['selected_company'] = company
#        fp = os.path.join(settings.BASE_DIR, 'static', 'qa', company_code, '*')
#        if settings.ENV_OS == 'windows':
#            fp = os.path.join(settings.BASE_DIR, 'app', 'static', 'qa', company_code, '*')
#        dirs = glob_files(fp=fp, recursive=True)
#        if settings.ENV_OS == 'windows':
#            dirs = reversed(dirs)

#        for dir in dirs:
#            dir_name.append(
#                {
#                    'dir_name':dir['dir_location'].split(os.path.sep)[-1],
#                    'dir_disp_name':datetime.fromtimestamp(float(dir['dir_location'].split(os.path.sep)[-1])),
#                    'count':dir['count']
#                }
#            )
#            if not selected_dir:
#                return HttpResponseRedirect('/qa/' + company_code + '?selected_dir=' + dir['dir_location'].split(os.path.sep)[-1])

#            if selected_dir and dir['dir_location'].split(os.path.sep)[-1] == selected_dir:
#                fp = os.path.join(settings.BASE_DIR, 'static', 'qa', company_code, selected_dir, '*')
#                if settings.ENV_OS == 'windows':
#                    fp = os.path.join(settings.BASE_DIR, 'app', 'static', 'qa', company_code, selected_dir, '*')
#                img_list = glob_files(fp=fp, recursive=False)
#                if img_list:
#                    for i,img in enumerate(img_list):
#                        if img.endswith(tuple(list_ext)):
#                        #for ext in list_ext:
#                        #    if img.split(os.path.sep)[-1].find(ext):
#                            #img_list[i] = str(img[img.find('/static'):]) if settings.ENV_OS == 'linux' else str(img[img.find('\static'):])
#                            fn = img.split(os.path.sep)[-1]
#                            img_list[i] = settings.STATIC_URL + 'qa/' + company_code + '/' + selected_dir + '/' + fn
#                else:
#                    img_list = {}

#    context['image_data'] = img_list
#    context['dir_list'] = dir_name
#    return render(
#        request,
#        context['template'],
#        context
#    )

#@api_view(['GET','POST'])
#@permission_classes([IsAuthenticated])
#def webhook(request, endpoint_name=None, company_code=None):
#    data = request.data
#    print(data)
#    #save_json(data, 'temp.json', 'app/data/rpt')
#    if endpoint_name == 'contentful':
#        from cms_tools import ingest_entry
#        if company_code == 'vys':
#            try:
#                ad = ingest_entry(data, endpoint_name, company_code)
#            except Exception as e:
#                lg.error(('Error: could not import', data))
#    return JsonResponse({}, status=200)

##REAL VYSTAR DATA FROM DEV (2 records below):
##{'metadata': {'tags': [{'sys': {'type': 'Link', 'linkType': 'Tag', 'id': 'finalytics'}}, {'sys': {'type': 'Link', 'linkType': 'Tag', 'id': 'productCarLoan'}}]}, 'sys': {'space': {'sys': {'type': 'Link', 'linkType': 'Space', 'id': 'kw2oi7dtt7lh'}}, 'id': '6ZTQNDSHo8orCtTJ1IOn59', 'type': 'Entry', 'createdAt': '2022-08-10T19:44:26.505Z', 'updatedAt': '2022-08-10T20:01:41.795Z', 'environment': {'sys': {'id': 'dev', 'type': 'Link', 'linkType': 'Environment'}}, 'publishedVersion': 15, 'publishedAt': '2022-08-10T19:50:05.510Z', 'firstPublishedAt': '2022-08-10T19:47:21.920Z', 'createdBy': {'sys': {'type': 'Link', 'linkType': 'User', 'id': '0U77BKpkbFF474k9yD7Orf'}}, 'updatedBy': {'sys': {'type': 'Link', 'linkType': 'User', 'id': '0U77BKpkbFF474k9yD7Orf'}}, 'publishedCounter': 3, 'version': 17, 'publishedBy': {'sys': {'type': 'Link', 'linkType': 'User', 'id': '0U77BKpkbFF474k9yD7Orf'}}, 'automationTags': [], 'contentType': {'sys': {'type': 'Link', 'linkType': 'ContentType', 'id': 'topicPromoContent'}}}, 'fields': {'name': {'en-US': 'Finalytics Car Loan Hero topic'}, 'image': {'en-US': {'sys': {'type': 'Link', 'linkType': 'Asset', 'id': '4MAMe21DpJZoTroewZcQDV'}}}, 'mobileImage': {'en-US': {'sys': {'type': 'Link', 'linkType': 'Asset', 'id': '4MAMe21DpJZoTroewZcQDV'}}}, 'header': {'en-US': 'Get a great car loan rate'}, 'body': {'en-US': {'nodeType': 'document', 'data': {}, 'content': [{'nodeType': 'paragraph', 'data': {}, 'content': [{'nodeType': 'text', 'value': "Apply now and get that new car you've always dreamed of.", 'marks': [], 'data': {}}]}]}}, 'links': {'en-US': [{'sys': {'type': 'Link', 'linkType': 'Entry', 'id': '7icNjKZFnBu8c4XPUQoqJB'}}, {'sys': {'type': 'Link', 'linkType': 'Entry', 'id': 'e8CAT6jVMb4BR6IoD8Lxl'}}]}}}
##{'metadata': {'tags': [{'sys': {'type': 'Link', 'linkType': 'Tag', 'id': 'finalytics'}}, {'sys': {'type': 'Link', 'linkType': 'Tag', 'id': 'productCarLoan'}}]}, 'sys': {'type': 'Entry', 'id': '6ZTQNDSHo8orCtTJ1IOn59', 'space': {'sys': {'type': 'Link', 'linkType': 'Space', 'id': 'kw2oi7dtt7lh'}}, 'environment': {'sys': {'id': 'dev', 'type': 'Link', 'linkType': 'Environment'}}, 'contentType': {'sys': {'type': 'Link', 'linkType': 'ContentType', 'id': 'topicPromoContent'}}, 'createdBy': {'sys': {'type': 'Link', 'linkType': 'User', 'id': '0U77BKpkbFF474k9yD7Orf'}}, 'updatedBy': {'sys': {'type': 'Link', 'linkType': 'User', 'id': '0U77BKpkbFF474k9yD7Orf'}}, 'revision': 4, 'createdAt': '2022-08-10T19:47:21.920Z', 'updatedAt': '2022-08-10T20:01:42.288Z'}, 'fields': {'name': {'en-US': 'Finalytics Car Loan Hero topic'}, 'image': {'en-US': {'sys': {'type': 'Link', 'linkType': 'Asset', 'id': '4MAMe21DpJZoTroewZcQDV'}}}, 'mobileImage': {'en-US': {'sys': {'type': 'Link', 'linkType': 'Asset', 'id': '4MAMe21DpJZoTroewZcQDV'}}}, 'header': {'en-US': 'Get a great car loan rate'}, 'body': {'en-US': {'data': {}, 'content': [{'data': {}, 'content': [{'data': {}, 'marks': [], 'value': "Apply now and get that new car you've always dreamed of.", 'nodeType': 'text'}], 'nodeType': 'paragraph'}], 'nodeType': 'document'}}, 'links': {'en-US': [{'sys': {'type': 'Link', 'linkType': 'Entry', 'id': '7icNjKZFnBu8c4XPUQoqJB'}}, {'sys': {'type': 'Link', 'linkType': 'Entry', 'id': 'e8CAT6jVMb4BR6IoD8Lxl'}}]}}}
##{'metadata': {'tags': [{'sys': {'id': 'websiteVCU', 'type': 'Link', 'linkType': 'Tag'}}]}, 'sys': {'space': {'sys': {'type': 'Link', 'linkType': 'Space', 'id': 'kw2oi7dtt7lh'}}, 'id': '5zDvhwQu8fF6pcfiMXl4I1', 'type': 'Entry', 'createdAt': '2022-08-30T17:31:12.457Z', 'updatedAt': '2022-08-31T14:05:27.018Z', 'environment': {'sys': {'id': 'master', 'type': 'Link', 'linkType': 'Environment'}}, 'createdBy': {'sys': {'type': 'Link', 'linkType': 'User', 'id': '4c6AvGXozgHqjvEND62dgA'}}, 'updatedBy': {'sys': {'type': 'Link', 'linkType': 'User', 'id': '3RKpEoc61W2pMdf9rVUVXo'}}, 'publishedCounter': 0, 'version': 22, 'automationTags': [], 'contentType': {'sys': {'type': 'Link', 'linkType': 'ContentType', 'id': 'topicBlog'}}}, 'fields': {'publicationDate': {'en-US': '2022-08-30T00:00'}, 'title': {'en-US': 'A picture of VyStar\xe2\x80\x99s past, present and future'}, 'slug': {'en-US': 'a-picture-of-vystars-past-present-and-future'}, 'pageTitle': {'en-US': 'A picture of VyStar\xe2\x80\x99s past, present and future'}, 'pageDescription': {'en-US': 'New mural adds color to credit union\xe2\x80\x99s campus.'}, 'cardImage': {'en-US': {'sys': {'type': 'Link', 'linkType': 'Asset', 'id': '14AGP8K5FbXysXv2yE0nQd'}}}, 'cardSummary': {'en-US': 'Read more about the newest addition to the VyStar Breezeway.'}, 'content': {'en-US': {'data': {}, 'content': [{'data': {}, 'content': [{'data': {}, 'marks': [], 'value': 'The space between the VyStar Tower and the VyStar Credit Union parking garage, known as the \xe2\x80\x9cVyStar Breezeway,\xe2\x80\x9d is more than a simple walkway. ', 'nodeType': 'text'}], 'nodeType': 'paragraph'}, {'data': {}, 'content': [{'data': {}, 'marks': [], 'value': 'With plentiful table and seating options, an open corridor and stage and several pieces of art, the area serves as a gathering space in downtown Jacksonville. Now, a new piece of art colors the wall overlooking the Breezeway. In August, VyStar unveiled a mural on the West Bay Tower painted by Jacksonville-based artist Anthony Rooney. ', 'nodeType': 'text'}], 'nodeType': 'paragraph'}, {'data': {}, 'content': [{'data': {}, 'marks': [], 'value': 'The mural ties VyStar\xe2\x80\x99s past, present and future together during its 70th year in business. ', 'nodeType': 'text'}], 'nodeType': 'paragraph'}, {'data': {}, 'content': [{'data': {}, 'marks': [{'type': 'bold'}], 'value': 'A nod toward VyStar\xe2\x80\x99s history', 'nodeType': 'text'}], 'nodeType': 'paragraph'}, {'data': {}, 'content': [{'data': {}, 'marks': [], 'value': 'The mural illustrates VyStar\xe2\x80\x99s story through a series of emblems. ', 'nodeType': 'text'}], 'nodeType': 'paragraph'}, {'data': {}, 'content': [{'data': {}, 'marks': [], 'value': 'In the background of the mural is the silhouette of Jacksonville\xe2\x80\x99s skyline, complete with the Main Street bridge and the skyscrapers \xe2\x80\x94 the VyStar Tower among them \xe2\x80\x94 that make up that view. VyStar\xe2\x80\x99s original name and logo, Jax Navy Federal Credit Union, is emblazoned just above the skyline. In the foreground, VyStar\xe2\x80\x99s newly redesigned logo is faintly imprinted over the scene, while four Blue Angels, the most striking and colorful piece of the mural, fly just out of frame. The Blue Angels are a fitting tribute for a credit union that was founded at Naval Air Station Jacksonville in 1952. ', 'nodeType': 'text'}], 'nodeType': 'paragraph'}, {'data': {}, 'content': [{'data': {}, 'marks': [], 'value': '\xe2\x80\x9cThe founding members are at the top of the mural looking toward  the Tower, which foreshadows what they were working towards and what VyStar eventually built up to,\xe2\x80\x9d said Rooney, who works alongside Jacksonville-based curation agency ArtRepublic. \xe2\x80\x9cAnd the Blue Angels represent the energy flowing through the whole thing, kind of guiding that progression. I really liked the idea that they can\xe2\x80\x99t be contained, so they\xe2\x80\x99re flying out of frame and moving forward into the future.\xe2\x80\x9d', 'nodeType': 'text'}], 'nodeType': 'paragraph'}, {'data': {}, 'content': [{'data': {}, 'marks': [], 'value': 'With the completion of this mural, Rooney adds another pin to the map he\xe2\x80\x99s painted across the city. The University of North Florida alumnus has been making his mark all over the First Coast since graduating with a bachelor\xe2\x80\x99s degree in Fine Art in 2011. In the years since, he\xe2\x80\x99s added a splash of color to several walls, including The Wall at College Park in Arlington. While his newest installation is noticeably different from his usual whimsical style, Rooney\xe2\x80\x99s touch is woven seamlessly into a picture of VyStar.', 'nodeType': 'text'}], 'nodeType': 'paragraph'}, {'data': {}, 'content': [{'data': {}, 'marks': [{'type': 'bold'}], 'value': 'Creating the mural', 'nodeType': 'text'}], 'nodeType': 'paragraph'}, {'data': {}, 'content': [{'data': {}, 'marks': [], 'value': 'The project has been in the making for just over a year, and the mural took roughly three weeks to create. At 30 feet by 70 feet, the mural is the largest project Rooney has ever completed. The area itself presented a unique challenge because of how limited access is to the wall.', 'nodeType': 'text'}], 'nodeType': 'paragraph'}, {'data': {}, 'content': [{'data': {}, 'marks': [], 'value': 'Rooney used image editing software to scale his artwork in a grid format from his initial design to its final position on the building. He also tested several different paints on bricks at his home and consulted with other mural artists to learn which paints would work best.', 'nodeType': 'text'}], 'nodeType': 'paragraph'}, {'data': {}, 'content': [{'data': {}, 'marks': [], 'value': 'The result is a new and unique depiction of VyStar\xe2\x80\x99s story. The VyStar parking garage, which houses even more artwork by ArtRepublic, offers the perfect vantage point for the finished work.', 'nodeType': 'text'}], 'nodeType': 'paragraph'}, {'data': {}, 'content': [{'data': {}, 'marks': [], 'value': '\xe2\x80\x9cSince we moved our operations into the VyStar Tower, we\xe2\x80\x99ve made focused efforts to create vibrant destinations in our community,\xe2\x80\x9d said EVP/Chief Operations Officer Chad Meadows. \xe2\x80\x9cFrom our collaboration with ArtRepublic to create a series of murals in the VyStar Tower parking garage to the newly unveiled mural in the VyStar Breezeway, we\xe2\x80\x99re proud to provide ample space to local artists in service of that goal. We continue to look for opportunities to contribute to the revitalization and development of downtown Jacksonville.\xe2\x80\x9d', 'nodeType': 'text'}], 'nodeType': 'paragraph'}, {'data': {}, 'content': [{'data': {}, 'marks': [], 'value': 'VyStar proudly welcomes the opportunity to brighten the places we call home, foster a culture of creativity and collaboration and support local artistry in all of its forms. Whether we\xe2\x80\x99re creating more inclusive, accessible experiences through music or lending our walls to new murals, we\xe2\x80\x99re thrilled to help make downtown a destination. ', 'nodeType': 'text'}], 'nodeType': 'paragraph'}], 'nodeType': 'document'}}, 'disclosures': {'en-US': [{'sys': {'type': 'Link', 'linkType': 'Entry', 'id': '24YdYf2GKUWQ6qPd4x6R6o'}}]}}}
##{'metadata': {'tags': [{'sys': {'type': 'Link', 'linkType': 'Tag', 'id': 'websiteVCU'}}]}, 'sys': {'space': {'sys': {'type': 'Link', 'linkType': 'Space', 'id': 'kw2oi7dtt7lh'}}, 'id': 'kjp1NtUJG8E4gvhKJBFPX', 'type': 'Entry', 'createdAt': '2022-08-29T19:53:44.222Z', 'updatedAt': '2022-08-31T14:14:19.379Z', 'environment': {'sys': {'id': 'master', 'type': 'Link', 'linkType': 'Environment'}}, 'createdBy': {'sys': {'type': 'Link', 'linkType': 'User', 'id': '0Salc25eiDvL4ycNphNROT'}}, 'updatedBy': {'sys': {'type': 'Link', 'linkType': 'User', 'id': '3RKpEoc61W2pMdf9rVUVXo'}}, 'publishedCounter': 0, 'version': 42, 'automationTags': [], 'contentType': {'sys': {'type': 'Link', 'linkType': 'ContentType', 'id': 'templateGeneric'}}}, 'fields': {'name': {'en-US': 'Page - Commercial Mortgage Promotion - 0822'}, 'slug': {'en-US': 'promotions/comm-mortgage-0822'}, 'pageTitle': {'en-US': 'Special low rates + No closing costs on commercial mortgages. | VyStar Credit Union'}, 'description': {'en-US': 'Local businesses help make our community a better place to live.'}, 'keywords': {'en-US': ['commercial mortgage']}, 'contentTitle': {'en-US': 'Special low rates + No closing costs on commercial mortgages.'}, 'content': {'en-US': {'data': {}, 'content': [{'data': {'target': {'sys': {'id': '61zzwKz1L6S4VXxgSi31HB', 'type': 'Link', 'linkType': 'Asset'}}}, 'content': [], 'nodeType': 'embedded-asset-block'}, {'data': {}, 'content': [{'data': {}, 'marks': [], 'value': 'Local businesses help make our community a better place to live. That\xe2\x80\x99s why we offer our members commercial mortgages with flexible loan terms. Like right now, VyStar is offering a special low rate on commercial mortgages for a fixed term with no closing costs.', 'nodeType': 'text'}], 'nodeType': 'paragraph'}, {'data': {}, 'content': [{'data': {}, 'content': [{'data': {}, 'content': [{'data': {}, 'marks': [], 'value': 'Rates as low as 4.64%(Owner-Occupied)*', 'nodeType': 'text'}], 'nodeType': 'paragraph'}], 'nodeType': 'list-item'}, {'data': {}, 'content': [{'data': {}, 'content': [{'data': {}, 'marks': [], 'value': 'Fixed-rate option for up to 15 years', 'nodeType': 'text'}], 'nodeType': 'paragraph'}], 'nodeType': 'list-item'}, {'data': {}, 'content': [{'data': {}, 'content': [{'data': {}, 'marks': [], 'value': 'Minimize your risk with longer amortization period and lower monthly payments', 'nodeType': 'text'}], 'nodeType': 'paragraph'}], 'nodeType': 'list-item'}, {'data': {}, 'content': [{'data': {}, 'content': [{'data': {}, 'marks': [], 'value': 'Save on fees: no origination fee and no closing costs up to 2% of the loan amount', 'nodeType': 'text'}], 'nodeType': 'paragraph'}], 'nodeType': 'list-item'}, {'data': {}, 'content': [{'data': {}, 'content': [{'data': {}, 'marks': [], 'value': 'Local underwriting means fast lending decisions', 'nodeType': 'text'}], 'nodeType': 'paragraph'}], 'nodeType': 'list-item'}, {'data': {}, 'content': [{'data': {}, 'content': [{'data': {}, 'marks': [], 'value': 'Cash-out refinance options', 'nodeType': 'text'}], 'nodeType': 'paragraph'}], 'nodeType': 'list-item'}, {'data': {}, 'content': [{'data': {}, 'content': [{'data': {}, 'marks': [], 'value': 'A team of dedicated commercial lending experts ready to help every step of the way.', 'nodeType': 'text'}], 'nodeType': 'paragraph'}], 'nodeType': 'list-item'}], 'nodeType': 'unordered-list'}, {'data': {}, 'content': [{'data': {}, 'marks': [], 'value': 'Whether you\xe2\x80\x99re currently renting your office space or need a bigger building to\\raccommodate your growing business, VyStar has commercial real estate loans\\rto meet your needs with a variety of financing options.', 'nodeType': 'text'}], 'nodeType': 'paragraph'}, {'data': {}, 'content': [{'data': {}, 'marks': [{'type': 'bold'}], 'value': 'Act now on this limited-time offer.', 'nodeType': 'text'}], 'nodeType': 'paragraph'}, {'data': {}, 'content': [{'data': {}, 'marks': [], 'value': 'Contact us to get started!', 'nodeType': 'text'}], 'nodeType': 'paragraph'}, {'data': {}, 'content': [{'data': {}, 'marks': [], 'value': 'Call our commercial lending team at ', 'nodeType': 'text'}, {'data': {'uri': 'tel:8004456289'}, 'content': [{'data': {}, 'marks': [{'type': 'bold'}], 'value': '800-445-6289', 'nodeType': 'text'}], 'nodeType': 'hyperlink'}, {'data': {}, 'marks': [], 'value': ' x 2292', 'nodeType': 'text'}], 'nodeType': 'paragraph'}, {'data': {}, 'content': [{'data': {}, 'marks': [], 'value': '', 'nodeType': 'text'}], 'nodeType': 'paragraph'}, {'data': {}, 'content': [{'data': {}, 'content': [{'data': {}, 'content': [{'data': {}, 'content': [{'data': {}, 'marks': [{'type': 'bold'}], 'value': 'Owner-Occupied Medical Facility', 'nodeType': 'text'}], 'nodeType': 'paragraph'}], 'nodeType': 'table-header-cell'}, {'data': {}, 'content': [{'data': {}, 'content': [{'data': {}, 'marks': [{'type': 'bold'}], 'value': 'Office/Flex Space', 'nodeType': 'text'}], 'nodeType': 'paragraph'}], 'nodeType': 'table-header-cell'}, {'data': {}, 'content': [{'data': {}, 'content': [{'data': {}, 'marks': [{'type': 'bold'}], 'value': 'Multifamily Residential', 'nodeType': 'text'}], 'nodeType': 'paragraph'}], 'nodeType': 'table-header-cell'}], 'nodeType': 'table-row'}, {'data': {}, 'content': [{'data': {}, 'content': [{'data': {}, 'content': [{'data': {}, 'marks': [{'type': 'bold'}], 'value': '$2,395,000', 'nodeType': 'text'}, {'data': {}, 'marks': [], 'value': '\\n15-Year Term\\n25-Year Amortization\\nPurchase', 'nodeType': 'text'}], 'nodeType': 'paragraph'}], 'nodeType': 'table-cell'}, {'data': {}, 'content': [{'data': {}, 'content': [{'data': {}, 'marks': [{'type': 'bold'}], 'value': '$2,200,000', 'nodeType': 'text'}, {'data': {}, 'marks': [], 'value': '\\n10-Year Term\\n25-Year Amortization\\nBank Refinance', 'nodeType': 'text'}], 'nodeType': 'paragraph'}], 'nodeType': 'table-cell'}, {'data': {}, 'content': [{'data': {}, 'content': [{'data': {}, 'marks': [{'type': 'bold'}], 'value': '$10,912,500', 'nodeType': 'text'}, {'data': {}, 'marks': [], 'value': '\\n10-Year Term\\n25-Year Amortization\\nPurchase', 'nodeType': 'text'}], 'nodeType': 'paragraph'}], 'nodeType': 'table-cell'}], 'nodeType': 'table-row'}], 'nodeType': 'table'}, {'data': {}, 'content': [], 'nodeType': 'hr'}, {'data': {}, 'content': [{'data': {}, 'marks': [{'type': 'italic'}], 'value': '\\n*Promotional rates only available for purchase and refinance of non-VyStar Credit Union business real estate loans. Borrower(s) and guarantor(s) must be a VyStar Credit Union member or become one prior to closing. All loans are subject to credit approval, and certain restrictions and limitations apply. For business loans to be eligible for the promotional rates, a complete loan package which includes the loan application, last 3-years of tax returns for the borrower (s) and guarantor(s), last 3-years of financial statements and a signed Personal Financial Statement (PFS) must be received no later than 10/31/2022 to qualify. An owner-occupied loan can be made for a property type where the Borrower occupies over 50% of the property\xe2\x80\x99s leasable space. Pre-payment penalties apply. Promotional rates only apply to business real estate loans with a maximum term of 15-years and a maximum amortization of 25-years and any applicable origination fees. Up to 2% of the loan amount paid towards closing costs. All additional closing costs and related expenses are the responsibility of the borrower and are to be paid at or prior to the closing. All credit union programs, rates, terms and conditions are subject to change at any time without notice.', 'nodeType': 'text'}], 'nodeType': 'paragraph'}, {'data': {}, 'content': [{'data': {}, 'marks': [{'type': 'italic'}], 'value': '\xc2\xa92022 VyStar Credit Union.', 'nodeType': 'text'}], 'nodeType': 'paragraph'}], 'nodeType': 'document'}}}}

##FAKE DATA FROM DEV (2 records below):
##{'metadata': {'tags': [{'sys': {'type': 'Link', 'linkType': 'Tag', 'id': 'finalytics'}}, {'sys': {'type': 'Link', 'linkType': 'Tag', 'id': 'productCarLoan'}}, {'sys': {'type': 'Link', 'linkType': 'Tag', 'id': 'test'}}]}, 'sys': {'type': 'Entry', 'id': '1y3VnAVaG9DPJ4JCa9zZe3', 'space': {'sys': {'type': 'Link', 'linkType': 'Space', 'id': 'vyx3a5x8y00y'}}, 'environment': {'sys': {'id': 'master', 'type': 'Link', 'linkType': 'Environment'}}, 'contentType': {'sys': {'type': 'Link', 'linkType': 'ContentType', 'id': 'hero'}}, 'createdBy': {'sys': {'type': 'Link', 'linkType': 'User', 'id': '0U77BKpkbFF474k9yD7Orf'}}, 'updatedBy': {'sys': {'type': 'Link', 'linkType': 'User', 'id': '0U77BKpkbFF474k9yD7Orf'}}, 'revision': 10, 'createdAt': '2022-06-29T19:24:42.027Z', 'updatedAt': '2022-06-29T19:44:18.650Z'}, 'fields': {'header': {'en-US': 'This is the car loan'}, 'secondaryHeader': {'en-US': 'Get great rates!'}}}

##{'metadata': {'tags': [{'sys': {'type': 'Link', 'linkType': 'Tag', 'id': 'dog'}}]}, 'sys': {'type': 'Asset', 'id': 'NHoVGFVSBHhV2FsVdGuXG', 'space': {'sys': {'type': 'Link', 'linkType': 'Space', 'id': 'vyx3a5x8y00y'}}, 'environment': {'sys': {'id': 'master', 'type': 'Link', 'linkType': 'Environment'}}, 'createdBy': {'sys': {'type': 'Link', 'linkType': 'User', 'id': '0U77BKpkbFF474k9yD7Orf'}}, 'updatedBy': {'sys': {'type': 'Link', 'linkType': 'User', 'id': '0U77BKpkbFF474k9yD7Orf'}}, 'revision': 5, 'createdAt': '2022-04-01T21:36:27.853Z', 'updatedAt': '2022-07-01T13:46:04.742Z'}, 'fields': {'title': {'en-US': 'Emmy'}, 'description': {'en-US': 'Testing 123 456'}, 'file': {'en-US': {'url': '//images.ctfassets.net/vyx3a5x8y00y/NHoVGFVSBHhV2FsVdGuXG/12c69da3f8e31f07e2461cec330ea378/emmy.png', 'details': {'size': 85370, 'image': {'width': 281, 'height': 279}}, 'fileName': 'emmy.png', 'contentType': 'image/png'}}}}