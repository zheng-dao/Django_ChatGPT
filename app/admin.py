from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django import forms
from .models import UserProfile
from .models import Company
#from .models import Account, AccountComment, Ad, AdCopy, AdTemplate, AnalyticsPlatform, AppReview, Asset, Benchmark, Campaign, Chart, ChartStyle, ChartType, City, Classification, Company, Competitor, Contact, Content, County, Daily, DataSummary, Demographic, DemographicCounty, Dimension, Domain, DomainKeywordGroup, FAQQuestion, FAQAnswer, GeoTarget, GlobalSetting, Ip, Keyword, KeywordGroup, NativeApp, Log, Location, Metric, MultiReport, NonFICompany, NotificationType, Notification, Offer, Page, PageKeyword, ParentKeyword, Rate, Report, RevenueKPI, Segment, Sheet, State, Subscription, SubscriptionPlan, Target, TestScenario, Tier, Tracking, UrlPattern, UrlSegment, VehicleMake, Version, WebAccount, WebProperty, WebToken, ZipCode
#from django.core import urlresolvers
#import modelclone
#from searchableselect.widgets import SearchableSelect
from django.utils.html import format_html
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.forms.widgets import TextInput
from app.views import check_company
admin.site.unregister(User)

##def the_callable(obj):
##    return u'<a href="#">link from the callable for {0}</a>'.format(obj)
##the_callable.allow_tags = True


def get_readonly_fields_func(self, request, obj=None):
    if not request.user.is_superuser:
        validate_groups = ['personalization_admin', 'personalization_staff']
        list_groups = request.user.groups.values_list('name', flat=True)
        groups_matching = [valid_grop for valid_grop in validate_groups if valid_grop in list_groups]
        if groups_matching:
            if obj:
                return self.readonly_fields + ['company',]
            # else:
            #     return self.readonly_fields + ['company',]
    return self.readonly_fields    




# def disable_company_field(self, request, obj=None, **kwargs):
#     print('request.user.is_superuser', request.user.is_superuser)
#     if not request.user.is_superuser:
#         validate_groups = ['personalization_admin', 'personalization_staff']
#         list_groups = request.user.groups.values_list('name', flat=True)
#         groups_matching = [valid_grop for valid_grop in validate_groups if valid_grop in list_groups]
#         if groups_matching:
#             kwargs['initial'] = request.user.userprofile.company
#             kwargs['disabled'] = True
#             kwargs['widget'] = forms.Select(attrs={'class': 'userprofile_select'})
#     return kwargs


def get_form_func(self, request, obj=None, model_name='ad', **kwargs):
    if isinstance(self, AdAdmin):
        form = super(AdAdmin, self).get_form(request, obj, **kwargs)
        if obj:
            # when user is login as superuser, superuser opens the existing ad, campaigns in listbox should be corresponding to the existing company.
            if request.user.is_superuser or request.user.email.lower().endswith(('@extractable.com', '@finalytics.ai')):
                form.base_fields['company'].initial = obj.company
                form.base_fields['campaigns'].queryset = Campaign.objects.filter(company=obj.company)
    elif isinstance(self, CampaignAdmin):
        form = super(CampaignAdmin, self).get_form(request, obj, **kwargs)
    if not request.user.is_superuser and not request.user.email.lower().endswith(('@extractable.com', '@finalytics.ai')):
        form.base_fields['company'].widget.attrs['class'] = 'capacity-css'
        form.base_fields['company'].disabled = True
        if obj is None: # new model form
            form.base_fields['company'].initial = request.user.userprofile.company
        if model_name == 'ad':
            form.base_fields['campaigns'].queryset = Campaign.objects.filter(company=request.user.userprofile.company)
    return form   

def reorder_company_field(self, request, obj=None, adminCls=None, **kwargs):
    fields = super(adminCls, self).get_fields(request, obj)
    if not request.user.is_superuser:
        validate_groups = ['personalization_admin', 'personalization_staff']
        list_groups = request.user.groups.values_list('name', flat=True)
        groups_matching = [valid_grop for valid_grop in validate_groups if valid_grop in list_groups]
        if groups_matching:
            fields.remove('company')
            fields.extend(['company'])
    return fields



def exclude_form_fields(self,override_class, request, obj, exclude_fields=None, **kwargs):
    if not request.user.is_superuser:
        validate_groups = ['personalization_admin', 'personalization_staff']
        list_groups = request.user.groups.values_list('name',flat = True)
        groups_matching = [valid_grop for valid_grop in validate_groups if valid_grop in list_groups]
        if groups_matching:
            if obj: 
                self.exclude = exclude_fields
    form = super(override_class, self).get_form(request, override_class, **kwargs)
    return form

def get_kwargs(user, user_type='staff'):
    kwargs = {}
    if user.email.lower().endswith(('@extractable.com', '@finalytics.ai')):
        pass
    elif user_type == 'staff':
        if user.is_staff == True and user.userprofile.company:
            kwargs['company'] = user.userprofile.company
    elif user_type == 'personalization_admin':
        if user_type in user.groups.all().values_list('name', flat=True) and user.is_staff == True and user.userprofile.company:
            kwargs['userprofile__company'] = user.userprofile.company
    return kwargs

def override_qs(self, override_class, request, user_type='staff'):
    co, ugs, context = check_company(request, {})
    request.GET._mutable = True
    request.GET.pop('cu_id', None)
    qs = super(override_class, self).get_queryset(request)
    if isinstance(self, Ad):
        qs = qs.prefetch_related('campaigns')
    kwargs = get_kwargs(request.user, user_type)
    if context['cu_id'] and context['is_fin_employee']:
        request.session['co'] = co  # to show the company name in sidebar
        if not request.session['cu_id'] == '':
            if override_class == UserAdmin:
                kwargs = {'userprofile__company': co}
            else:
                kwargs = {'company': co}
    if kwargs:
        return qs.filter(**kwargs)
    return qs

def create_contexts(context, help_dict, ext='_id', replace_text=None):
    for key, value in help_dict.iteritems():
        if 'tk_link' in value and context['original'] and isinstance(context['original'], dict):
            #print context['original'].__dict__
            #print key, key + ext, value
            #print 'adminform:'
            #print context['adminform'].__dict__
            if replace_text:
                tk_link = context['original'].__dict__[replace_text]
            else:
                tk_link = context['original'].__dict__[key + ext]
            #request.resolver_match.args[0]
            value = value.replace('tk_link', str(tk_link))
        if key not in context['adminform'].readonly_fields:
            context['adminform'].form.fields[key].help_text = value
    return context

#def exclude_fields(allsets, exclude):
#    for i, fieldset in enumerate(allsets):
#        fields_temp = fieldset[1]['fields']
#        fields_role = [x for x in fields_temp if x not in exclude]
#        allsets[i][1]['fields'] = fields_role
#    return allsets

#def exclude_fieldsets(fieldsets, exclude):
#    for i, set in enumerate(fieldsets):
#        if set[0] in exclude:
#            del fieldsets[i]
#    return fieldsets

#class AccountCommentInline(admin.TabularInline):
#    model = AccountComment
#    extra =1

#class FAQAnswerInline(admin.TabularInline):
#    model = FAQAnswer
#    extra = 3

#class LocationInline(admin.TabularInline):
#    model = Location

#class SubscriptionInline(admin.TabularInline):
#    model = Subscription

#class TestScenarioInline(admin.StackedInline):
#    model = TestScenario
#    extra = 0
#    classes = ['collapse']

class UserProfileInline(admin.StackedInline):
    model = UserProfile

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'company':
            if not request.user.is_superuser:
                validate_groups = ['personalization_admin', 'personalization_staff']
                list_groups = request.user.groups.values_list('name', flat=True)
                groups_matching = [valid_grop for valid_grop in validate_groups if valid_grop in list_groups]
                if groups_matching:
                    kwargs['initial'] = request.user.userprofile.company
                    kwargs['disabled'] = True
                    kwargs['widget'] = forms.Select(attrs={'class': 'userprofile_select'})

        return super(UserProfileInline, self).formfield_for_dbfield(db_field, request, **kwargs)

    def get_fields(self, request, obj=None, **kwargs):
        return reorder_company_field(self, request, obj, UserProfileInline, **kwargs)        

#class AccountAdmin(admin.ModelAdmin):
#    fieldsets = [
#        ('Core Fields', {
#            'fields': ['account_type','owner','contact','company','is_active'],
#        }),
#        ('Billing Info', {
#            'fields': ['billing_first_name','billing_last_name','billing_email_address','billing_phone','billing_address_line1','billing_address_line2','billing_unit_number','billing_city','billing_state_abbrev','billing_zip_code','billing_zip_4code','billing_country'],
#            'classes': ['collapse'],
#        }),
#        ('Other Fields', {
#            'fields': ['date_deactivated', 'deactivated_intentionally'],
#            'classes': ['collapse'],
#        }),
#    ]
#    inlines = [AccountCommentInline, SubscriptionInline]
#    list_display = ('getaccountnames', 'id','account_type','company', 'is_active', 'billing_zip_code')
#    list_filter = ['is_active', 'billing_city','account_type','paid_status','billing_zip_code']
#    ordering = ['-timestamp_modified']
#    search_fields = ['contact__contact_first_name','contact__last_name','contact__email_address','contact__zip_code','billing_zip_code','billing_last_name','company__name']
#    raw_id_fields = ['owner', 'contact']
#    autocomplete_lookup_fields = {
#        'aou': ['owner'],
#        'aoc': ['contact'],
#    }
#    def getaccountnames(self, obj):
#        if obj.company:
#            returnstr = '%s' % (obj.company)
#        elif obj.contact:
#            returnstr = '%s %s %s' % (obj.contact.first_name, obj.contact.last_name, obj.contact.email_address)
#        else:
#            returnstr = 'None'
#        return returnstr
#    getaccountnames.short_description = "Name"


#class AdAdmin(admin.ModelAdmin):
#    save_as = True
#    readonly_fields = ['timestamp_modified', 'timestamp_created']
#    autocomplete_fields = ['company', 'keyword_group', 'ad_template']
#    list_display = ['name', 'company', 'is_active', 'keyword_group', 'ad_method', 'div_id', 'div_class', 'ordinal', 'content_type', 'get_campaigns', 'pages', 'is_active']
#    list_filter = ['is_active', ('company', admin.RelatedOnlyFieldListFilter,) , 'delivery_type', 'div_id', 'content_type', 'category', 'subcategory', ('keyword_group', admin.RelatedOnlyFieldListFilter,)]
#    filter_horizontal = ['campaigns']
#    search_fields = ['name', 'company__name', 'pages', 'ad_html', 'id']
#    raw_id_fields = ('company',)
#    ordering = ['-timestamp_modified']
#    inlines = [TestScenarioInline]

    



#    #fieldsets = [
#    #    ('', {
#    #        'fields': ['company', 'campaigns', 'is_active', 'is_biz', 'keyword_group', 'content_type', 'category', 'subcategory', 'pages', 'ad_method', 'delivery_type', 'div_id', 'div_class', 'ordinal', 'div_type', 'img_to_replace', 'ad_html', 'start_dt', 'end_dt'],
#    #    }),
#    #]

#    def get_form(self, request, obj=None, **kwargs):
#        return get_form_func(self, request, obj, 'ad', **kwargs)

#    def get_fields(self, request, obj=None, **kwargs):
#        return reorder_company_field(self, request, obj, AdAdmin, **kwargs)

#    # def get_readonly_fields(self, request, obj=None):
#    #     return get_readonly_fields_func(self, request, obj)
 
    
#    # def get_readonly_fields(self, request, obj=None):
#    #     readonly_fields = super().get_readonly_fields(request, obj)
#    #     if obj:
#    #         readonly_fields += ("company",)
#    #     return readonly_fields

#    def get_queryset(self, request):
#        return override_qs(self, AdAdmin, request, 'staff')
    
#    def get_campaigns(self, obj):
#        return ", ".join([c.name for c in obj.campaigns.all()])

#class AdCopyAdmin(admin.ModelAdmin):
#    save_as = True
#    list_display = ['templates', 'headline', 'company', 'keyword_group', 'headline', 'link_label']
#    list_filter = ['templates', 'keyword_group']
#    search_fields = ['headline', 'company__name', 'body_copy']
#    raw_id_fields = ('company',)
#    ordering = ['-timestamp_modified']

#    def get_queryset(self, request):
#        return override_qs(self, AdCopyAdmin, request, 'staff')


#class AdTemplateAdmin(admin.ModelAdmin):
#    save_as = True
#    list_display = ['template_name', 'company', 'ad_method', 'div_id']
#    list_filter = [('company', admin.RelatedOnlyFieldListFilter,), 'ad_method']
#    search_fields = ['template_name']
#    raw_id_fields = ('company',)
#    ordering = ['-timestamp_modified']

#    # def get_form(self, request, obj=None, **kwargs):
#    #     return disable_company_field(self, request, obj, AdTemplateAdmin, **kwargs)

#    def formfield_for_dbfield(self, db_field, request, **kwargs):
#        if db_field.name == 'company':
#            if not request.user.is_superuser:
#                validate_groups = ['personalization_admin', 'personalization_staff']
#                list_groups = request.user.groups.values_list('name', flat=True)
#                groups_matching = [valid_grop for valid_grop in validate_groups if valid_grop in list_groups]
#                if groups_matching:
#                    kwargs['initial'] = request.user.userprofile.company
#                    kwargs['disabled'] = True
#                    kwargs['widget'] = forms.Select(attrs={'class': 'userprofile_select'})

#        return super(AdTemplateAdmin, self).formfield_for_dbfield(db_field, request, **kwargs)

#    def get_fields(self, request, obj=None, **kwargs):
#        return reorder_company_field(self, request, obj, AdTemplateAdmin, **kwargs)

#    def get_queryset(self, request):
#        return override_qs(self, AdTemplateAdmin, request, 'staff')






#class AnalyticsPlatformAdmin(admin.ModelAdmin):
#    fields = ['code', 'name', 'api_name', 'label', 'version', 'current_year', 'current_qtr', 'current_month']
#    list_display = ['code', 'name', 'label', 'version']
#    ordering = ['-timestamp_modified']

#class AppReviewAdmin(admin.ModelAdmin):
#    list_display = ['napp', 'username', 'score', 'content', 'dt']
#    list_filter = ['napp__app_type', 'score', 'napp']
#    search_fields = ['napp__company__name', 'version_reviewed']
#    ordering = ['-dt']

#class AssetAdmin(admin.ModelAdmin):
#    save_as = True
#    readonly_fields = ['timestamp_created', 'timestamp_created']
#    autocomplete_fields = ['company', 'domain', 'keyword_group', ]
#    list_display = ['company', 'alt_text', 'filename', 'div_ids', 'keyword_group', 'demographics', 'asset_type', 'short_url']
#    list_filter = ['is_active', ('company', admin.RelatedOnlyFieldListFilter,) , 'asset_type', 'content_type', 'keyword_group', 'category', 'subcategory']
#    search_fields = ['company__name', 'demographics', 'div_ids', 'short_url', 'alt_text']
#    ordering = ['-timestamp_modified']

#    def get_queryset(self, request):
#        return override_qs(self, AssetAdmin, request, 'staff')

#class BenchmarkAdmin(admin.ModelAdmin):
#    list_display = ['name', 'benchmark_type', 'benchmark_type_id', 'avg', 'sum', 'min', 'max', 'count', 'model_name']
#    list_filter = ['ap', 'model_name', 'benchmark_type', 'benchmark_type_id']
#    search_fields = ['name', 'ap__name', 'benchmark_type', 'benchmark_type_id']
#    ordering = ['-timestamp_modified']

#class CampaignAdmin(admin.ModelAdmin):
#    save_as = True
#    autocomplete_fields = ['company']
#    list_display = ['name', 'company', 'is_active', 'mode', 'partial_delivery_percent']
#    list_filter = ['is_active', ('company', admin.RelatedOnlyFieldListFilter,), 'mode', 'campaign_type', 'always_remember_users_for_partial_delivery']
#    search_fields = ['name', 'company__name']
#    ordering = ['-timestamp_modified']
#    raw_id_fields = ('company',)

#    #fieldsets = [
#    #    ('', {
#    #        'fields': ['name','company','is_active','partial_delivery_percent','always_remember_users_for_partial_delivery','pages','start_dt','end_dt'],
#    #    }),
#    #]    

#    def get_readonly_fields(self, request, obj=None):
#        return get_readonly_fields_func(self, request, obj)
        
            
#    def get_form(self, request, obj=None, **kwargs):
#        return get_form_func(self, request, obj, 'campaign', **kwargs)    

#    def get_queryset(self, request):
#        return override_qs(self, CampaignAdmin, request, 'staff')   

#class ChartForm(forms.ModelForm):
#    class Meta:
#        model = Chart
#        exclude = ()
#        widgets = {
#            #'metrics': SearchableSelect(model='app.Metric', search_field='name', limit=10),
#            'dimensions': SearchableSelect(model='app.Dimension', search_field='name', limit=10),
#            'sheets': SearchableSelect(model='app.Sheet', search_field='name', limit=10),
#        }

#class ChartAdmin(admin.ModelAdmin):
#    fields = ['name', 'is_free', 'charttype', 'chartstyle', 'style_override', 'metrics', 'extra_instance_fields', 'extra_instance_field_labels', 'order_by', 'dimensions', 'sheets', 'embed_code']
#    #filter_horizontal = ['metrics']
#    list_display = ['name', 'id', 'charttype', 'chartstyle', 'is_free']
#    list_filter = ['charttype']
#    search_fields = ['name', 'charttype__name', 'is_free']
#    ordering = ['-timestamp_modified']
#    #raw_id_fields = ('metrics','dimensions')
#    form = ChartForm

#class ChartTypeAdmin(admin.ModelAdmin):
#    fields = ['name', 'chart_type', 'chartstyle']
#    list_display = ['name', 'chart_type', 'chartstyle']
#    list_filter = ['chart_type']
#    search_fields = ['name', 'chart_type']
#    ordering = ['-timestamp_modified']

#class ChartStyleAdmin(admin.ModelAdmin):
#    fields = ('name', 'chart_type', 'highcharts_style')
#    list_display = fields
#    ordering = ['-timestamp_modified']

#class CityAdmin(admin.ModelAdmin):
#    search_fields = ['name']

#class ClassificationAdmin(admin.ModelAdmin):
#    list_display = [field.name for field in Classification._meta.get_fields()]
#    list_filter = ['system_name', 'year']
#    search_fields = ['name', 'system_name', 'code']
#    ordering = ['seq_number']

class CompanyAdmin(admin.ModelAdmin):
    fields = ['name', 'parse', 'aliases', 'alias_google_sheets', 'number','code','subcode','company_type','is_subscriber','is_client','is_prospect', 'ga_timezone', 'wp_preview_enabled', 'js_version', 'js_scripts_enabled', 'platform_mode', 'top_us_fi', 'top_state_fi', 'scrape_demo_base_url', 'is_active', 'personalization_is_active', 'personalize_all_pages', 'use_login_to_infer_member', 'biz_enabled', 'override_personal_categorization', 'use_firttime_ml_model', 'firttime_ml_model_mode', 'use_firsttime_lifetime_value', 'general_personalization_is_active', 'custom_personalization_is_active', 'search_results_page', 'search_query_parameter', 'account_summary_url', 'account_summary_parser', 'trxn_url', 'trxn_parser', 'expiring_balance_to_pmt_ratio', 'distressed_percent', 'partial_delivery_percent', 'always_remember_users_for_partial_delivery', 'use_revenue_model', 'use_branch_model', 'use_rate_model', 'offer_type', 'cycle_date','join_number','rssd','cu_type','city','state','charterstate','state_code','zip_code','four_code','county_code','cong_dist','states_operating_in','smsa','attention_of','street','region','se','district','year_opened','tom_code','limited_inc','issue_date','peer_group','quarter_flag']
    list_display = ['name','number','code','company_type','is_subscriber', 'is_prospect', 'personalization_is_active']
    list_filter = ['company_type', 'is_subscriber','is_client','is_active', 'personalization_is_active', 'top_us_fi', 'top_state_fi', 'state']
    search_fields = ['number','name','company_type','code','id','zip_code']
    ordering = ['-is_subscriber', '-timestamp_modified']

#class NonFIAdmin(CompanyAdmin):
#    pass

#class CompetitorAdmin(admin.ModelAdmin):
#    fields = ['company', 'competitor']
#    #filter_horizontal = ['competitors']
#    list_display = ['company', 'competitor', 'overlap', 'common_keywords', 'sort']
#    list_filter = ['company__is_subscriber','company__is_client']
#    search_fields = ['company__name','competitors']
#    ordering = ['-timestamp_modified']

#class ContentAdmin(admin.ModelAdmin):
#    save_as = True
#    list_display = ['company', 'category', 'subcategory', 'trigger_value', 'headline', 'body_copy']
#    list_filter = ['is_active', 'category', 'subcategory', ('company', admin.RelatedOnlyFieldListFilter,)]
#    search_fields = ['trigger_value', 'headline', 'body_copy']
#    ordering = ['-timestamp_modified']

#class ContactAdmin(admin.ModelAdmin):
#    fieldsets = [
#        ('Core Fields', {
#            'fields': ['category','subcategory','first_name','last_name','company_id','title','zip_code','location'],
#        }),
#        ('Contact Info', {
#            'fields': ['email_address','email_address2','email_address3','phone_default','phone_default_type','phone_landline','phone_work','phone_mobile','phone_alt1','phone_alt2','fax'],
#            'classes': ['collapse'],
#        }),
#        ('Other Fields', {
#            'fields': ['added_by_uid'],
#            'classes': ['collapse'],
#        }),
#    ]
#    list_display = ('first_name','last_name','email_address','phone_mobile','zip_code','id')
#    list_filter = ['contact_type','category','subcategory']
#    search_fields = ['id','first_name','last_name','email_address','email_address2','email_address3','phone_mobile','phone_default','zip_code']
#    ordering = ('-timestamp_modified',)

#class CountyAdmin(admin.ModelAdmin):
#    list_display = ['name', 'state_abbrev', 'population_2019', 'population_2018', 'population_2017']
#    list_filter = ['state_abbrev']
#    search_fields = ['name']

#class DailyAdmin(admin.ModelAdmin):
#    #fields = ('date', 'series','series_id','entity_id','total')
#    list_display = ['date', 'entity_type', 'entity_id', 'series_id', 'series', 'analyticsplatform', 'total', 'ga_userType', 'ga_pageviews', 'ga_pagePath']
#    list_filter = ['analyticsplatform', 'entity_type', 'ga_userType']
#    search_fields = ['series', 'series_id', 'entity_id']
#    ordering = ['-timestamp_modified']

#class DataSummaryAdmin(admin.ModelAdmin):
#    #fields = ('series','series_id','series_type','entity_id','state','entity_type','entity_subtype','entity_subtype_id','year','base_data_interval','total','q1','q2','q3','q4','analyticsplatform','custom')
#    list_display = ['entity_id', 'series', 'series_id', 'year', 'q1', 'q2', 'q3', 'q4', 'total', 'entity_type', 'state', 'analyticsplatform', 'entity_subtype_id']
#    list_filter = ['analyticsplatform', 'year', 'series_type', 'entity_type', 'entity_subtype', 'series', 'state', 'entity_subtype_id']
#    search_fields = ['id', 'series', 'year', 'series_id', 'entity_id', 'entity_subtype', 'entity_subtype_id']
#    ordering = ['-timestamp_modified']

#class DemographicAdmin(admin.ModelAdmin):
#    #fields = ['name', 'label', 'analyticsplatform']
#    list_display = ['zipcode', 'city', 'state', 'average_house_value', 'median_age', 'income_per_household', 'population', 'population_estimate']
#    list_filter = ['state']
#    search_fields = ['zipcode', 'city', 'state']
#    ordering = ['-timestamp_modified']

#class DemographicCountyAdmin(admin.ModelAdmin):
#    #fields = ['name', 'label', 'analyticsplatform']
#    list_display = ['county', 'state_abbrev', 'year', 'naics', 'employees', 'establishments', 'annual_payroll', 'q1_annual_payroll']
#    list_filter = ['year', 'state_abbrev']
#    search_fields = ['county__name']
#    ordering = ['naics']

#class DimensionAdmin(admin.ModelAdmin):
#    fields = ['name', 'label', 'analyticsplatform']
#    list_display = ['name', 'analyticsplatform', 'label']
#    list_filter = ['analyticsplatform']
#    search_fields = ['label', 'name', 'analyticsplatform__name']
#    ordering = ['-timestamp_modified']

#class DomainAdmin(admin.ModelAdmin):
#    #fields = ['company', 'name', 'asset_tier', 'web', 'email', 'is_subdomain', 'ga_view_id', 'embed_code', 'parent_of_subdomain', 'total_assets', 'total_members', 'total_assets_scaled', 'total_members_scaled', 'domain_authority_per_asset', 'domain_authority_per_member', 'domain_authority', 'domain_authority_per_asset_scaled', 'domain_authority_per_member_scaled', 'overall_loading_experience', 'overall_loading_experience_mobile', 'total_loans', 'total_loans_amount', 'avg_loan_amount', 'growth_rate']
#    list_display = ['name', 'link', 'total_assets_rank', 'total_assets', 'monthly_adwords_budget', 'seo_value_estimate', 'ppc_value_estimate', 'root_domains_to_root_domain', 'organic_clicks_per_month', 'paid_clicks_per_month', 'domain_authority', 'total_assets', 'total_assets_rank', 'total_members', 'outperform_da_per_asset', 'outperform_da_per_member', 'growth_rate', 'spam_score', 'ga_view_id']
#    list_filter = ['company__company_type', 'web','email','is_subdomain','asset_tier']
#    search_fields = ['company__name', 'name', 'ga_view_id']
#    ordering = ['-timestamp_modified']

#    def link(self, obj):
#        return format_html("<a href='https://{name}' target='_blank'>Go</a>", name=obj.name)

#    link.short_description = "Link"

#class DomainKeywordGroupAdmin(admin.ModelAdmin):
#    list_display = ['domain', 'keyword_group', 'total_volume_potential', 'total_clicks', 'ppc_total_volume_potential', 'ppc_total_clicks', 'total_volume_potential_scaled', 'total_clicks_scaled', 'ppc_total_volume_potential_scaled', 'ppc_total_clicks_scaled']
#    list_filter = ['domain__company__company_type', 'keyword_group__is_core_product', 'keyword_group__keyword']
#    search_fields = ['domain__name', 'keyword_group__keyword']
#    ordering = ['-timestamp_modified']

#class FAQAnswerAdmin(admin.ModelAdmin):
#    list_display = ['faqquestion', 'atext']
#    list_filter = [('faqquestion__domain__company', admin.RelatedOnlyFieldListFilter,), 'faqquestion__qcat', 'faqquestion__keyword_group']
#    search_fields = ['atext', 'faqquestion__qtext']

#class FAQQuestionAdmin(admin.ModelAdmin):
#    fields = ['domain', 'qtype', 'keyword_group', 'qcat', 'qsubcat', 'is_internal', 'is_live', 'qtext', 'qorder']
#    inlines = [FAQAnswerInline]
#    list_display = ['qtext','qcat','qsubcat','qorder', 'is_internal', 'is_live', 'domain']
#    list_filter = [('domain__company', admin.RelatedOnlyFieldListFilter,), 'qtype','qcat','qsubcat', 'keyword_group__keyword']
#    search_fields = ['qtext', 'keyword_group__keyword']

#class GeoTargetAdmin(admin.ModelAdmin):
#    list_display = ('name','canonical_name','ga_id','country_code','target_type')
#    list_filter = ['target_type','state_abbrev','country_code']
#    search_fields = ['name', 'canonical_name', 'ga_id']

#class GlobalSettingAdmin(admin.ModelAdmin):
#    save_as = True
#    autocomplete_fields = ['company']
#    readonly_fields = ['setting_value_long']
#    #fields = ['setting_app_version', 'setting_name', 'setting_type', 'setting_category', 'setting_subcategory', 'setting_timing', 'setting_value', 'setting_units', 'setting_value_long', 'setting_desc']
#    list_display = ('company', 'setting_name', 'setting_value', 'setting_category', 'setting_subcategory', 'setting_order','setting_units','setting_app_version','timestamp_modified')
#    list_filter = [('company', admin.RelatedOnlyFieldListFilter,), 'setting_type','setting_category','setting_subcategory','setting_app_version']
#    search_fields = ['setting_name', 'setting_desc']
#    ordering = ['-timestamp_modified']

#class IpAdmin(admin.ModelAdmin):
#    list_display = ('ip','company','zipcode','city','state','organization')
#    list_filter = [('company', admin.RelatedOnlyFieldListFilter,), 'state']
#    search_fields = ['ip', 'zipcode', 'city', 'organization']
#    ordering = ['-timestamp_modified']

#class KeywordAdmin(admin.ModelAdmin):
#    #fields = ['keyword', 'clicks', 'ctr', 'monthly_volume', 'is_active', 'is_primary', 'is_category', 'is_biz', 'is_bank', 'is_investment', 'is_general', 'is_location', 'is_rate']
#    list_display = ['keyword', 'keywordSEODifficulty', 'clicks', 'monthly_volume', 'ctr', 'clicks_scaled', 'monthly_volume_scaled', 'ctr_scaled']
#    list_filter = ['is_active', 'is_core_product', 'is_primary', 'is_category', 'is_biz', 'is_bank', 'is_investment', 'is_general', 'is_location', 'is_rate', 'audience']
#    search_fields = ['keyword']
#    ordering = ['-timestamp_modified']


#class KeywordGroupAdmin(admin.ModelAdmin):
#    save_as = True
#    #fields = ['keyword', 'is_core_product']
#    #filter_horizontal = ['related_keyword']
#    list_display = ['keyword', 'category', 'is_core_product', 'max_total_volume_potential', 'max_total_clicks', 'ppc_max_total_volume_potential', 'ppc_max_total_clicks']
#    list_filter = ['is_core_product', 'is_biz', 'rate_type', 'category', 'subcategory']
#    search_fields = ['keyword', 'category', 'subcategory']
#    ordering = ['-timestamp_modified']


#class ParentKeywordAdmin(admin.ModelAdmin):
#    list_display = ['child_keyword', 'child_keyword_label', 'parent_keyword']
#    list_filter = ['is_top_level', 'is_core_product', 'parent_keyword__child_keyword']
#    search_fields = ['child_keyword', 'parent_keyword__child_keyword']
#    ordering = ['-timestamp_modified']

#class LocationAdmin(admin.ModelAdmin):
#    save_as = True
#    list_display = ('physicaladdressline1', 'company','physicaladdresscity','physicaladdressstatecode','physicaladdresspostalcode',)
#    list_filter = ['company__company_type', 'physicaladdressstatecode']
#    search_fields = ['physicaladdresscity','physicaladdresspostalcode','physicaladdressstatecode', 'company__name'] #,'contact__first_name','contact__last_name']
#    ordering = ('-timestamp_modified',)
#    #raw_id_fields = ['contact']
#    #autocomplete_lookup_fields = {
#    #    'id': ['contact'],
#    #}
#    #date_hierarchy = 'stall_id'
#    #def save_model(self, request, obj, form, change):
#    #    if not obj.pk: # call super method if object has no primary key 
#    #        super(LocationAdmin, self).save_model(request, obj, form, change)
#    #    else:
#    #        pass # don't actually save the parent instance

#    #def save_formset(self, request, form, formset, change):
#    #    formset.save() # this will save the children
#    #    form.instance.save() # form.instance is the parent

#class LogAdmin(admin.ModelAdmin):
#    readonly_fields = ['post_json', 'timestamp_modified', 'timestamp_created']
#    autocomplete_fields = ['company']
#    list_display = ['company', 'post_json']
#    list_filter = [('company', admin.RelatedOnlyFieldListFilter,)]
#    search_fields = ['post_json']
#    ordering = ['-timestamp_modified']

#class MetricAdmin(admin.ModelAdmin):
#    #fields = ['name', 'label', 'code', 'unit', 'subtype', 'model','analyticsplatform', 'is_benchmark', 'is_derivative', 'is_suffix']
#    list_display = ['name', 'analyticsplatform','model', 'label', 'is_benchmark', 'is_derivative']
#    list_filter = ['analyticsplatform', 'is_benchmark', 'is_derivative', 'model', 'subtype']
#    search_fields = ['label', 'name', 'analyticsplatform__name','model']
#    ordering = ['-timestamp_modified']

#class MultiReportAdmin(admin.ModelAdmin):
#    #fields = ['name', 'is_active', 'report']
#    list_display = ['name', 'id', 'is_active']
#    list_filter = ['is_active', 'report']
#    search_fields = ['name', 'report']
#    ordering = ['-timestamp_modified']

#class NativeAppAdmin(admin.ModelAdmin):
#    list_display = ['company', 'app_name', 'app_type', 'app_score', 'app_version']
#    list_filter = ['app_type']
#    search_fields = ['napp__company__name', 'app_version']
#    raw_id_fields = ('company',)
#    ordering = ['-timestamp_modified']

#class NotificationAdmin(admin.ModelAdmin):
#    readonly_fields = ['timestamp_modified']
#    fields = ['user_id','username','to','note_type','channels','product','template','extra_content','from_email','subject','body_is_json','body','is_read','is_sent','queue','persist','attempts','attempts_pattern','priority','must_dismiss','is_global','batch_id','do_not_disturb','expires','mode','task_id']
#    list_display = ['user_id', 'username', 'to', 'note_type', 'product', 'template', 'timestamp_modified'] #'body_is_json', 'is_sent', 
#    list_filter = ['product','channels','template'] #'is_sent', 'body_is_json', 
#    search_fields = ['note_type','product','template']
#    ordering = ('note_type',)

#class NotificationTypeAdmin(modelclone.ClonableModelAdmin):
#    fields = ['note_type','note_site','is_test','is_active','do_not_disturb','email_flag','sms_flag','mobile_app_flag','web_app_flag','product','use_dynamic_template','template','extra_content','from_email','body','subject','is_read','queue','persist','attempts','attempts_pattern','priority','must_dismiss','is_global','batch_id','expires','mode']
#    list_display = ['note_type', 'product', 'template','is_test', 'is_active']
#    list_filter = ['is_active','is_test','product','template','email_flag','sms_flag','mobile_app_flag','web_app_flag']
#    search_fields = ['note_type','product','template']
#    ordering = ('-timestamp_modified',)

##class PageListFilter(admin.SimpleListFilter):
##    title = 'Companies'
##    parameter_name = 'domain__id'
##    default_status = None
##    def lookups(self, request, model_admin):
##        qs = model_admin.get_queryset(request)
##        options = ()
##        qs = qs.values_list('domain__id', 'domain__company__name').exclude(domain__company__code=None).exclude(domain__company__code='')
##        return sorted(list(set(qs)), key = lambda x: x[1])

##    def queryset(self, request, queryset):
##        return queryset.exclude(domain__company__code=None).exclude(domain__company__code='')

#class OfferAdmin(admin.ModelAdmin):
#    save_as = True
#    list_display = ['headline', 'company', 'keyword_group', 'headline', 'link_label']
#    list_filter = ['company', 'keyword_group']
#    search_fields = ['headline', 'company__name', 'body_copy', 'keyword_group__keyword']
#    raw_id_fields = ('company',)
#    ordering = ['-timestamp_modified']

#    def get_queryset(self, request):
#        return override_qs(self, OfferAdmin, request, 'staff')

#class PageAdmin(admin.ModelAdmin):
#    save_as = True
#    autocomplete_fields = ['domain']

#    list_display = ['domain', 'link', 'url', 'category', 'attributes', 'url_type', 'ga_pageviews', 'date_updated', 'overall_performance_category', 'load_performance', 'load_speed_ms', 'load_speed_score']
#    #list_filter = [PageListFilter, 'is_domain', 'is_app_start', 'is_app_complete', 'overall_performance_category', 'url_type', 'category', 'subcategory']
#    list_filter = ['is_biz', 'category', ('domain__company', admin.RelatedOnlyFieldListFilter,), 'subcategory', 'is_domain', 'is_app_start', 'is_app_complete', 'overall_performance_category', 'url_type', ]
#    search_fields = ['url', 'overall_performance_category', 'domain__name']
#    ordering = ['-timestamp_modified']

#    def company_code(self, obj):
#        return Company.objects.filter(is_active=True).exclude(company__code=None)

#    def link(self, obj):
#        if obj.domain:
#            return format_html("<a href='https://{domain_name}{url}' target='_blank'>Go</a>", url=obj.url, domain_name=obj.domain.name)
#        else:
#            return ''

#    link.short_description = "Link"

#class PageKeywordAdmin(admin.ModelAdmin):
#    list_display = ['keyword', 'link', 'exact_local_monthly_search_volume', 'monthly_clicks', 'value_per_month', 'link_url', 'position', 'ppc_position', 'exact_clicks_per_day', 'seo_difficulty', 'date_updated']
#    list_filter = ['page__is_domain']
#    search_fields = ['page__url', 'keyword__keyword']
#    ordering = ['-timestamp_modified']

#    def link(self, obj):
#        if obj.page and obj.page.url:
#            return format_html("<a href='https://{url}' target='_blank'>Go</a>", url=obj.page.url)
#        return ''

#    def link_url(self, obj):
#        if obj.page and obj.page.url:
#            return format_html(str(obj.page.url))
#        return ''

#    link.short_description = "Link"

#class RateAdmin(admin.ModelAdmin):
#    save_as = True
#    list_display = ('product', 'entity_id', 'entity_type', 'keyword_group', 'year', 'q1', 'q2', 'q3', 'q4')
#    list_filter = ['entity_type', 'year', 'keyword_group', 'product']
#    search_fields = ['product', 'keyword_group__keyword', 'entity_id']
#    ordering = ['-timestamp_modified']

#class ReportAdmin(admin.ModelAdmin):
#    fields = ['name', 'is_active', 'chart', 'layout']
#    list_display = ['name', 'id', 'is_active']
#    list_filter = ['is_active', 'chart']
#    search_fields = ['name', 'chart']
#    ordering = ['-timestamp_modified']

##class RevenueKPIForm(forms.ModelForm):
##    class Meta:
##        model = RevenueKPI
##        #fields = '__all__'
##        exclude = ()
##        widgets = {
##            'domain': SearchableSelectSelect(model='app.Domain', search_field='name', limit=10),
##        }

#class RevenueKPIAdmin(admin.ModelAdmin):
#    save_as = True
#    autocomplete_fields = ['domain', 'keyword_group']
#    list_display = ['domain', 'keyword_group', 'revenue_per_member', 'conversion_rate']
#    list_filter = ['keyword_group__is_core_product', 'keyword_group__keyword']
#    #filter_horizontal = ['domain']
#    search_fields = ['domain__name', 'domain__company__name', 'keyword_group__keyword']
#    ordering = ['-timestamp_modified']
#    #form = RevenueKPIForm
#    raw_id_fields = ['domain']
#    autocomplete_lookup_fields = {
#        'domain': ['name'],
#    }

#class SheetForm(forms.ModelForm):
#    class Meta:
#        model = Sheet
#        exclude = ()
#        widgets = {
#            'metrics': SearchableSelect(model='app.Metric', search_field='name', limit=10),
#            'dimensions': SearchableSelect(model='app.Dimension', search_field='name', limit=10),
#        }

#class SegmentAdmin(admin.ModelAdmin):
#    list_display = ['name', 'entity_source', 'short_desc', 'entity_type']
#    list_filter = ['entity_source', 'entity_type', 'income', 'age_ranges', 'employment_levels', 'education_levels']
#    search_fields = ['name', 'description', 'short_desc']
#    ordering = ['entity_id']

#class UrlSegmentAdmin(admin.ModelAdmin):
#    #fields = ['name', 'is_active', 'chart', 'layout']
#    list_display = ['guessed_category', 'category', 'guessed_subcategory', 'link_text', 'segment', 'splits']
#    list_filter = ['is_biz', 'is_rate', 'is_calculator', 'guessed_category', 'category']
#    search_fields = ['segment', 'splits', 'link_text', 'guessed_category', 'category']
#    ordering = ['-timestamp_modified']

#class SheetAdmin(admin.ModelAdmin):
#    fields = ['name', 'is_active', 'tab', 'range', 'sheet_id', 'has_header', 'timeframe_type', 'timeframe_start', 'timeframe_end', 'metrics', 'dimensions']
#    list_display = ['name', 'tab', 'range', 'sheet_id', 'timeframe_type', 'is_active']
#    list_filter = ['is_active']
#    search_fields = ['name', 'tab', 'range']
#    ordering = ['-timestamp_modified']
#    form = SheetForm

#class StateAdmin(admin.ModelAdmin):
#    list_display = ['name', 'population_2021', 'percent_us_population', 'population_density_mi2', 'population_rank_2021']
#    search_fields = ['name', 'state_abbrev']
#    ordering = ['name']

#class SubscriptionPlanAdmin(admin.ModelAdmin):
#    fields = list(set([f.name for f in SubscriptionPlan._meta.fields]) - set(['id','timestamp_created', 'timestamp_modified']))
#    exclude = ['timestamp_created', 'timestamp_modified']
#    list_display = ('plan_id', 'plan_type', 'account', 'interval', 'start_date', 'end_date',)
#    list_filter = ['plan_type']
#    search_fields = ['plan_type', 'plan_id', 'account__contact__last_name', 'account__contact__zip_code']
#    ordering = ('-timestamp_modified',)
#    raw_id_fields = ['account']
#    autocomplete_lookup_fields = {
#        'aid': ['account'],
#    }

#class SubscriptionAdmin(admin.ModelAdmin):
#    fields = list(set([f.name for f in Subscription._meta.fields]) - set(['id','timestamp_created', 'timestamp_modified']))
#    list_display = ('subscription_id', 'subscriptionplan', 'account', 'is_active',)
#    list_filter = ['is_active']
#    search_fields = ['subscription_id', 'subscriptionplan', 'account__contact__last_name', 'account__contact__zip_code']
#    ordering = ('-timestamp_modified',)
#    raw_id_fields = ['account']
#    autocomplete_lookup_fields = {
#        'aid': ['account'],
#    }

#class TargetAdmin(admin.ModelAdmin):
#    save_as = True
#    ordering = ('-timestamp_modified',)

#class TestScenarioAdmin(admin.ModelAdmin):
#    save_as = True
#    autocomplete_fields = ['company', 'ad']
#    list_display = ('name', 'company', 'category', 'ad')
#    list_filter = [('company', admin.RelatedOnlyFieldListFilter,), 'is_demo', 'is_test', 'is_active', 'category']
#    search_fields = ['name', 'company__name']
#    ordering = ('-timestamp_modified',)

#    #def get_queryset(self, request):
#    #    return override_qs(self, TestScenarioAdmin, request, 'staff')
        
#    #def get_form(self, request, obj=None, **kwargs):
#    #    exclude_fields = ("company",)
#    #    return exclude_form_fields(self,TestScenarioAdmin, request, obj, exclude_fields, **kwargs)

#    #def render_change_form(self, request, context, *args, **kwargs):
#    #    qs = Ad.objects.none()
#    #    CU_groups = ['personalization_admin','personalization_staff']
#    #    company = request.user.userprofile.company
#    #    current_user_groups = request.user.groups.values_list('name', flat=True).first()
#    #    if (request.user.is_staff and not request.user.is_superuser ) and (current_user_groups in CU_groups):
#    #        qs = Ad.objects.filter(company=company)
#    #    elif request.user.is_superuser:
#    #        qs = Ad.objects.all()

#        #form = override_change_form_func(self, TestScenarioAdmin, 'ad', qs, request, context, *args, **kwargs)
#        #return form    

#class TierAdmin(admin.ModelAdmin):
#    list_display = ('name', 'tier', 'min_assets', 'max_assets',)

#class TrackingAdmin(admin.ModelAdmin):
#    readonly_fields = ['timestamp_created', 'timestamp_modified']
#    list_display = ('company', 'campaign', 'ad', 'impressions', 'clicks', 'timestamp_modified')

#class WebAccountAdmin(admin.ModelAdmin):
#    list_display = ('account', 'account_type', 'user', 'external_account_id', 'token',)
#    list_filter = ('account', 'account_type', 'external_account_id',)
#    search_fields = ('account__company__name', 'external_account_id',)
#    ordering = ('-timestamp_modified',)

#class WebPropertyAdmin(admin.ModelAdmin):
#    list_display = ('url', 'external_property_id', 'view_id', 'name',)
#    list_filter = ('webaccount',)
#    search_fields = ('url', 'view_id',)
#    ordering = ('-timestamp_modified',)

#class WebTokenAdmin(admin.ModelAdmin):
#    list_display = ('token', 'refresh_token',)
#    list_filter = ('webaccount',)
#    search_fields = ('webaccount__account',)
#    ordering = ('-timestamp_modified',)

#class ZipCodeAdmin(admin.ModelAdmin):
#    list_display = ('code', 'city', 'state_abbrev',)
#    list_filter = ('location_type', 'state_abbrev',)
#    search_fields = ('code', 'city',)

#class UrlPatternAdmin(admin.ModelAdmin):
#    list_display = ('domain', 'pattern', 'order', 'url_type', 'attributes', 'exclude_list')
#    list_filter = ('url_type',)

#class UserAdmin(UserAdmin):
#    readonly_fields = ('id',)
#    #def view_link(self, obj):
#    #    return u"<a href='/review_terms?uid=%d'>Go</a>" % obj.id
#    #view_link.short_description = 'Review Terms'
#    #view_link.allow_tags = True

#    list_display = ['id', 'email', 'date_joined', 'first_name', 'last_name', 'is_active','is_superuser','username'] #'view_link', 
#    list_filter = ('is_active', 'is_staff', 'is_superuser', 'userprofile__send_test_msgs', 'groups')
#    inlines = [ UserProfileInline, ]
#    ordering = ('-id',)

#    def get_queryset(self, request):
#        return override_qs(self, UserAdmin, request, 'personalization_admin')
#        #qs = super(UserAdmin, self).get_queryset(request)
#        #if request.user.groups.all():
#        #    user_groups = list(request.user.groups.all().values_list('name', flat=True))
#        #    if 'personalization_admin' in user_groups:
#        #        return qs.filter(Q(is_staff=True, userprofile__company__id=request.user.userprofile.company.id, groups__name="personalization_staff") | Q(is_staff=False, is_superuser=False, email=''))
#        #return qs

#    #def render_change_form(self, request, context, *args, **kwargs):
#    #    help_dict = {
#    #        'username':'<a href="/review_terms?uid=tk_link">Review Terms</a>',
#    #        }
#    #    contexts = create_contexts(context, help_dict, ext='')
#    #    return super(UserAdmin, self).render_change_form(request, context, args, kwargs)

#class VehicleMakeAdmin(admin.ModelAdmin):
#    list_display = ['name', 'parse', 'vehicle_type', 'aliases']
#    search_fields = ['name', 'parse', 'aliases']
#    list_filter = ['is_active', 'vehicle_type']
#    ordering = ['-timestamp_modified']

#class VersionAdmin(admin.ModelAdmin):
#    #readonly_fields = ['timestamp_modified', 'timestamp_created']
#    #fields = ['version']
#    list_display = ['version', 'release_name', 'timestamp_modified', 'timestamp_created']
#    ordering = ['-id']

##(admin.ModelAdmin):
##    list_display = ('email', 'username', 'first_name', 'last_name')
##    list_filter = ('is_active', 'is_staff', 'is_superuser')
##    search_fields = ('email',)
##    inlines = [ UserProfileInline, ]
##    ordering = ('-date_joined',)


admin.site.register(User, UserAdmin)
##admin.site.register(User, UserProfileAdmin)
#admin.site.register(Account, AccountAdmin)
#admin.site.register(Ad, AdAdmin)
#admin.site.register(AdCopy, AdCopyAdmin)
#admin.site.register(AdTemplate, AdTemplateAdmin)
#admin.site.register(AnalyticsPlatform, AnalyticsPlatformAdmin)
#admin.site.register(AppReview, AppReviewAdmin)
#admin.site.register(Asset, AssetAdmin)
#admin.site.register(Benchmark, BenchmarkAdmin)
#admin.site.register(Campaign, CampaignAdmin)
#admin.site.register(Chart, ChartAdmin)
#admin.site.register(ChartStyle, ChartStyleAdmin)
#admin.site.register(ChartType, ChartTypeAdmin)
#admin.site.register(City, CityAdmin)
#admin.site.register(Classification, ClassificationAdmin)
admin.site.register(Company, CompanyAdmin)
#admin.site.register(Competitor, CompetitorAdmin)
#admin.site.register(Contact, ContactAdmin)
#admin.site.register(Content, ContentAdmin)
#admin.site.register(County, CountyAdmin)
#admin.site.register(Daily, DailyAdmin)
#admin.site.register(DataSummary, DataSummaryAdmin)
#admin.site.register(Demographic, DemographicAdmin)
#admin.site.register(DemographicCounty, DemographicCountyAdmin)
#admin.site.register(Dimension, DimensionAdmin)
#admin.site.register(Domain, DomainAdmin)
#admin.site.register(DomainKeywordGroup, DomainKeywordGroupAdmin)
#admin.site.register(FAQAnswer, FAQAnswerAdmin)
#admin.site.register(FAQQuestion, FAQQuestionAdmin)
#admin.site.register(GeoTarget, GeoTargetAdmin)
#admin.site.register(GlobalSetting, GlobalSettingAdmin)
#admin.site.register(Ip, IpAdmin)
#admin.site.register(Keyword, KeywordAdmin)
#admin.site.register(KeywordGroup, KeywordGroupAdmin)
#admin.site.register(ParentKeyword, ParentKeywordAdmin)
#admin.site.register(Location, LocationAdmin)
#admin.site.register(Log, LogAdmin)
#admin.site.register(Metric, MetricAdmin)
#admin.site.register(MultiReport, MultiReportAdmin)
#admin.site.register(NativeApp, NativeAppAdmin)
#admin.site.register(NonFICompany, NonFIAdmin)
#admin.site.register(Notification, NotificationAdmin)
#admin.site.register(NotificationType, NotificationTypeAdmin)
#admin.site.register(Offer, OfferAdmin)
#admin.site.register(Page, PageAdmin)
#admin.site.register(PageKeyword, PageKeywordAdmin)
#admin.site.register(Rate, RateAdmin)
#admin.site.register(Report, ReportAdmin)
#admin.site.register(RevenueKPI, RevenueKPIAdmin)
#admin.site.register(Segment, SegmentAdmin)
#admin.site.register(Sheet, SheetAdmin)
#admin.site.register(State, StateAdmin)
#admin.site.register(Subscription, SubscriptionAdmin)
#admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
#admin.site.register(Target, TargetAdmin)
#admin.site.register(TestScenario, TestScenarioAdmin)
#admin.site.register(Tier, TierAdmin)
#admin.site.register(Tracking, TrackingAdmin)
#admin.site.register(VehicleMake, VehicleMakeAdmin)
#admin.site.register(Version, VersionAdmin)
#admin.site.register(WebAccount, WebAccountAdmin)
#admin.site.register(WebProperty, WebPropertyAdmin)
#admin.site.register(WebToken, WebTokenAdmin)
#admin.site.register(UrlPattern, UrlPatternAdmin)
#admin.site.register(UrlSegment, UrlSegmentAdmin)
#admin.site.register(ZipCode, ZipCodeAdmin)

