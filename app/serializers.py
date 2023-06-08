from rest_framework import serializers
from app.models import Account, Ad, AnalyticsPlatform, Campaign, Chart, ChartStyle, ChartType, Company, Contact, DataSummary, Domain, FAQQuestion, FAQAnswer, GlobalSetting, Keyword, KeywordGroup, Location, Metric, MultiReport, Notification, Page, ParentKeyword, Report, RevenueKPI, Sheet, Subscription, SubscriptionPlan, TestScenario, Tier, User, UserProfile
#from allauth.account.models import EmailAddress, EmailConfirmation
#from allauth.account.adapter import DefaultAccountAdapter
#from app.forms import UserForm
#from django.http import HttpRequest
#import account_tools
#import allocator
#from djgeojson.serializers import Serializer as GeoJSONSerializer

from . import chart_utils
from . import chart_builder

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        #fields = '__all__'
        fields = ('account_type', 'owner', 'contact', 'company', 'paid_status', 'billing_first_name', 'billing_last_name', 'billing_address_line1', 'billing_address_line2', 'billing_unit_number', 'billing_city', 'billing_state_abbrev', 'billing_zip_code', 'billing_zip_4code', 'is_active', 'added_by_uid')

class AnalyticsPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsPlatform
        fields = ('id','code', 'name', 'label', 'api_name')

class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ('div_id', 'ad_method', 'ad_html')
        read_only_fields = fields

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'

class ChartStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartStyle
        fields = ('chart_type', 'name', 'highcharts_style')

class ChartTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartType
        fields = ('chart_type', 'name', 'chartstyle')

class ChartSerializer(serializers.ModelSerializer):
    chart_data = serializers.SerializerMethodField()
    charttype = ChartTypeSerializer(many=False, read_only=True)
    #chartstyle = ChartStyleSerializer(many=False)
    class Meta:
        model = Chart
        fields = ('id', 'name', 'is_free', 'embed_code', 'charttype', 'chart_data',)
        #fields = ('id','charttype', 'name', 'is_free', 'chartstyle', 'metrics', 'dimensions','embed_code','chart_data',)
        read_only_fields = fields

    def _previous_chart_rendering(self, instance):
        try:
            request = self.context['request']
            entity_id = request.query_params.get('entity_id', None)
            entity_type = request.query_params.get('entity_type', None)
            entity_subtype_id = request.query_params.get('entity_subtype_id', None)
            entity_subtype = request.query_params.get('entity_subtype', None)
            dimensions = request.query_params.get('dimensions', None)
            map_dimensions = request.query_params.get('map', None)
            start_year = request.query_params.get('start_year', None)
            daily_span = request.query_params.get('daily_span', None)
            show_competitors = request.query_params.get('show_competitors', None)
            show_multiple = request.query_params.get('show_multiple', False)
            is_free = request.query_params.get('is_free', None)
            if start_year:
                start_year = int(start_year)
            end_year = request.query_params.get('end_year', None)
            if end_year:
                end_year = int(end_year)
            if daily_span and daily_span.isdigit():
                daily_span = int(daily_span)
            as_combo = request.query_params.get('as_combo', None)
            kwargs = {
                'entity_id': entity_id,
                'entity_type': entity_type,
                'entity_subtype_id': entity_subtype_id,
                'entity_subtype': entity_subtype,
                'dimensions': dimensions,
                'map_dimensions': map_dimensions,
                'start_year': start_year,
                'end_year': end_year,
                'daily_span': daily_span,
                'show_competitors': int(show_competitors) if show_competitors else False,
                'show_multiple': int(show_multiple) if show_multiple else False
            }
            kwargs['is_free'] = is_free
            for i in list(kwargs.keys()):
                if kwargs[i] is None:
                    del kwargs[i]
            if as_combo:
                kwargs.pop('entity_id', None)
                return chart_utils.build_combo_chart(instance.pk, entity_id, chart = instance, **kwargs)
            return chart_utils.process_get_chart_data(instance, **kwargs)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print('cant get chart', e)

    def get_chart_data(self, instance):
        already_rendered = self.context.get('already_rendered',None)
        if already_rendered:
            return None
        request = self.context['request']
        use_new =  request.query_params.get('use_new',False)
        if use_new:
            request_dict = request.query_params.dict()
            request_dict['chart_id'] = str(instance.pk)
            charts = chart_builder.get_chart_from_request(request_dict)
            return charts[0] if len(charts)>0 else None
        return self._previous_chart_rendering(instance)
            
        #return None

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'code', 'number', 'name', 'company_type', 'is_active', 'is_client', 'state', 'zip_code')
        read_only_fields = fields

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'contact_type', 'category', 'subcategory','first_name','last_name', 'email_address', 'phone_default', 'phone_default_type', 'phone_landline', 'phone_work', 'phone_mobile', 'fax', 'title')

class DataSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSummary
        fields = ('id', 'series', 'series_id', 'series_type', 'entity_id', 'entity_type', 'entity_subtype', 'entity_subtype_id', 'q1', 'q2', 'q3', 'q4', 'total')
        read_only_fields = fields

class DomainSerializer(serializers.ModelSerializer):
    company = CompanySerializer(many=False)
    class Meta:
        model = Domain
        fields = ('company', 'name', 'web', 'email', 'is_subdomain', 'ga_view_id', 'embed_code', 'parent_of_subdomain', 'total_assets', 'total_assets_rank', 'growth_rate', 'growth_rate_rank', 'total_members', 'total_members_rank', 'domain_authority_per_asset', 'domain_authority_per_member', 'outperform_da_per_asset', 'outperform_da_per_member', 'assets_per_member', 'assets_per_member_rank', 'spam_score', 'spam_score_rank', 'avg_loan_amount', 'avg_loan_amount_rank', 'root_domains_to_root_domain', 'root_domains_to_root_domain_rank', 'domain_authority', 'domain_authority_rank', 'overall_loading_experience', 'overall_loading_experience_mobile', 'external_pages_to_root_domain', 'external_pages_to_root_domain_rank')
        read_only_fields = fields

class FAQQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQQuestion
        fields = ('qtype', 'qcat', 'qsubcat', 'qtext', 'qorder')

class FAQAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQAnswer
        fields = ('qid', 'atext', 'file1', 'aorder', 'timestamp_modified')

class GlobalSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalSetting
        fields = ('id','setting_app_version','setting_name','setting_type','setting_functional_group','setting_category','setting_subcategory','setting_timing','setting_value','setting_value_long','timestamp_created','timestamp_modified')

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['keyword', 'clicks', 'ctr', 'monthly_volume', 'clicks_scaled', 'ctr_scaled', 'monthly_volume_scaled', 'is_active', 'is_primary', 'is_category', 'is_biz', 'is_bank', 'is_investment', 'is_general', 'is_location', 'is_rate']
        read_only_fields = fields

class KeywordGroupSerializer(serializers.ModelSerializer):
    related_keyword = KeywordSerializer(many=True)
    class Meta:
        model = KeywordGroup
        fields = ['keyword', 'code', 'is_free', 'is_core_product', 'related_keyword']
        read_only_fields = fields

    def to_representation(self, instance):
        data =  super().to_representation(instance)
        related_limit = self.context.get('related_limit',None)
        if related_limit:
            data['related_keyword'] = data['related_keyword'][:related_limit]
        return data
    
class ParentParentKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentKeyword
        fields = ['id', 'child_keyword', 'child_keyword_label', 'is_top_level', 'is_core_product']
        read_only_fields = fields

class ParentKeywordSerializer(serializers.ModelSerializer):
    parent_keyword = ParentParentKeywordSerializer(many=False)
    class Meta:
        model = ParentKeyword
        fields = ['id', 'child_keyword', 'child_keyword_label', 'parent_keyword', 'is_top_level', 'is_core_product']
        read_only_fields = fields

class PageKGSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeywordGroup
        fields = ['keyword', 'is_free']
        read_only_fields = fields

class PageDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ['name']
        read_only_fields = fields

class PageSerializer(serializers.ModelSerializer):
    keyword_group = PageKGSerializer(many=False)
    domain = PageDomainSerializer(many=False)
    class Meta:
        model = Page
        fields = ('url', 'url_type', 'screenshot_url', 'domain', 'keyword_group', 'ppc_value_estimate','ppc_value_estimate','ppc_clicks_estimate','ppc_num_results','seo_value_estimate','seo_traffic_estimate','seo_num_results','overall_performance_category','load_performance','load_speed_ms','load_speed_score','overall_performance_category_mobile','load_performance_mobile','load_speed_ms_mobile','load_speed_score_mobile', 'ga_entrances', 'ga_exits', 'ga_uniquePageviews',)
        read_only_fields = fields

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id','address_line1','address_line2', 'latitude', 'longitude')

class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ('name', 'label', 'analyticsplatform')

class MultiReportSerializer(serializers.ModelSerializer):
    report = serializers.SerializerMethodField()
    class Meta:
        model = Report
        fields = ('name', 'report', 'is_active', 'layout')
        read_only_fields = fields
    
    def get_report(self, instance):
        request = self.context['request']
        reports = instance.report.all()
        already_rendered = False
        return  ReportSerializer(reports, many=True, context=self.context).data

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    chart = serializers.SerializerMethodField()
    class Meta:
        model = Report
        fields = ('name', 'chart', 'is_active', 'layout')
        read_only_fields = fields
    
    def get_chart(self, instance):
        request = self.context['request']
        charts = instance.chart.all()
        already_rendered = False
        use_new =  request.query_params.get('use_new', False)
        if use_new:
            request_dict = request.query_params.dict()
            #print(request_dict)
            for index, chart in enumerate(instance.chart.all()):
                request_dict[f'chart_id_{index+1}'] = str(chart.pk)
            charts_data = chart_builder.get_chart_from_request(request_dict)
            already_rendered = True
            response = []
            total = len(charts)
            for index, chart in enumerate(charts):
                result = ChartSerializer(chart,context={**self.context,**{'already_rendered':True}}).data
                result['chart_data'] = charts_data[index]
                response.append(result)
            return response

        return  ChartSerializer(charts, many=True, context=self.context).data

class RevenueKPISerializer(serializers.ModelSerializer):
    domain = DomainSerializer(many=False)
    keyword_group = PageKGSerializer(many=False)
    class Meta:
        model = RevenueKPI
        fields = ('domain', 'keyword_group', 'revenue_per_member', 'conversion_rate')
        read_only_fields = fields

class SheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sheet
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('id', 'account', 'subscriptionplan', 'user_id','start_date','end_date', 'recur_automatically', 'original_plan_start_date', 'trial_id', 'discount_id', 'coupon_id', 'status', 'is_active')

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ('id', 'plan_id', 'plan_type','start_date','end_date', 'name', 'interval', 'amount', 'is_active')

class TestScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestScenario
        fields = '__all__'

class TierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tier
        fields = ('name', 'tier', 'min_assets', 'max_assets')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'first_name', 'last_name', 'is_staff')

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'contact_id', 'email_is_confirmed')


