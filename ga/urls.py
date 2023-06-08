#from datetime import datetime
from django.conf import settings
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
#from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from rest_framework import routers, serializers, viewsets
#from two_factor.gateways.twilio.urls import urlpatterns as tf_twilio_urls
#from two_factor.urls import urlpatterns as tf_urls
##admin.site.index_template = 'admin/layout_admin.html'
admin.autodiscover()
##admin.site.enable_nav_sidebar = False
##from rest_framework.authtoken import views
##from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
#from app.views import AccountViewSet, AdViewSet, AnalyticsPlatformViewSet, CampaignViewSet, ChartViewSet, ChartStyleViewSet, ChartTypeViewSet, CompanyViewSet, ContactViewSet, DataSummaryViewSet, DomainViewSet, FAQQuestionViewSet, FAQAnswerViewSet, GlobalSettingViewSet, LocationViewSet, MetricViewSet, NotificationViewSet, KeywordGroupViewSet, MultiReportViewSet, MySetupCompleteView, ParentKeywordViewSet, PageViewSet, ReportViewSet, RevenueKPIViewSet, SheetViewSet, SubscriptionViewSet, SubscriptionPlanViewSet, TestScenarioViewSet, TierViewSet, UserViewSet, UserProfileViewSet


from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from app.forms import BootstrapAuthenticationForm
##import app
from django.contrib.auth import views as auth_views
##admin.site.index_template = 'admin/layout_admin.html'
##admin.autodiscover()

from django.views.generic.base import TemplateView
from allauth.account.views import ConfirmEmailView

##from two_factor.admin import AdminSiteOTPRequired
##admin.site.__class__ = AdminSiteOTPRequired

urlpatterns = [
#    path('robots.txt', TemplateView.as_view(template_name='app/robots.txt', content_type='text/plain'),),
    url(r'^account/login/$', RedirectView.as_view(url='/account/login', permanent=False), name='login'),
    url(r'^account/$', RedirectView.as_view(url='/account', permanent=False), name='account'),
    url(r'^account/email/$', RedirectView.as_view(url='/account/email', permanent=False), name='email'),
    url(r'^login/$', RedirectView.as_view(url='/account/login', permanent=False), name='login'),
    url(r'^admin/login/', RedirectView.as_view(url='/account/login', permanent=False), name='admin_login'),
    url(r'^admin/logout/', RedirectView.as_view(url='/account/logout', permanent=False), name='admin_logout'),

    path('dashboard', views.dashboard, name='dashboard'),
#    path('a/dashboard', TemplateView.as_view(template_name='admin_static/dashboard.html'), name='a-dashboard'),
#    path('choose-company', views.choose_company, name='choose-company'),

#    path('ai-settings/algorithms', TemplateView.as_view(template_name='admin/algorithms.html'), name='algorithms-enabled'),
#    path('ai-settings/products', views.products_list, name='products_list'),
#    path('ai-settings/products/delete/<int:product_id>', views.products_list, name='delete_product'),
#    path('ai-settings/update-products-order-ajax', views.update_products_order_ajax, name="update_products_order_ajax"),
    
#    path('ai-settings/segments/delete/<int:segment_id>', views.segments_list, name='delete_segment'),
#    path('ai-settings/segments', views.segments_list, name='segments'),
#    path('ai-settings/keywords', views.keywords_list, name='keywords'),
#    # path('ai-settings/keywords', TemplateView.as_view(template_name='admin_static/keywords.html'), name='keywords'),
#    path('ai-settings/charter-region', views.charter_region_map, name='charter'),

#    path('a/ai-settings/algorithms', TemplateView.as_view(template_name='admin_static/algorithms.html'), name='a-algorithms-enabled'),
#    path('a/ai-settings/products', TemplateView.as_view(template_name='admin_static/products.html'), name='a-products_list'),
#    path('a/ai-settings/segments', TemplateView.as_view(template_name='admin_static/segments.html'), name='a-segments'),
#    path('a/ai-settings/simple-segments', TemplateView.as_view(template_name='admin_static/simple_segments.html'), name='a-simple-segments'),
#    path('a/ai-settings/ftv-segment', TemplateView.as_view(template_name='admin_static/ftv-segment.html'), name='a-ftv-segment'),
#    path('a/ai-settings/keywords', TemplateView.as_view(template_name='admin_static/keywords.html'), name='a-keywords'),
#    path('a/ai-settings/charter-region', views.charter_region_map, name='a-charter'),


#    path('scenarios/scenarios', TemplateView.as_view(template_name='admin_static/scenarios.html'), name='scenarios'),
#    path('scenarios/create-new-scenario', TemplateView.as_view(template_name='admin_static/create-new-scenario.html'), name='create-new-scenario'),
#    path('scenarios/fi-scenarios', TemplateView.as_view(template_name='admin_static/fi-scenarios.html'), name='fi-scenarios'),

#    path('a/scenarios/create-new-scenario', TemplateView.as_view(template_name='admin_static/create-new-scenario.html'), name='a-create-new-scenario'),
#    path('a/scenarios/scenarios', TemplateView.as_view(template_name='admin_static/scenarios.html'), name='a-scenarios'),
#    path('a/scenarios/fi-scenarios', TemplateView.as_view(template_name='admin_static/fi-scenarios.html'), name='a-fi-scenarios'),


#    path('scenarios/branch-events', views.branch_events, name="branch_events"),
#    # path('b/create-branch-event', views.create_branch_event, name="create_branch_event"),
#    path('scenarios/create-zc-json', views.create_zc_json, name="create_zc_json"),
#    # path('b/list-counties', views.list_counties, name="list_counties"),
#    path('scenarios/create-branch-event', views.create_branch_event, name="create_branch_event"),
#    path('scenarios/list-counties', views.list_counties, name="list_counties"),
#    path('scenarios/zipcodes-template-selection', views.zipcodes_template_selection, name="zipcodes_template_selection"),
#    path('scenarios/ad-settings', views.ad_settings, name="ad_settings"),

#    path('a/scenarios/branch-events', views.branch_events, name="a-branch_events"),
#    path('a/scenarios/create-zc-json', views.create_zc_json, name="a-create_zc_json"),
#    path('a/scenarios/create-branch-event', views.create_branch_event, name="a-create_branch_event"),
#    path('a/scenarios/list-counties', views.list_counties, name="a-list_counties"),
#    path('a/scenarios/zipcodes-template-selection', views.zipcodes_template_selection, name="a-zipcodes_template_selection"),
#    path('a/scenarios/ad-settings', views.ad_settings, name="a-ad_settings"),
    

#    path('campaign-type', views.campaign_type, name='campaign_type'),
#    path('campaign-content-modules', views.campaign_content_modules, name='campaign_content_modules'),
#    path('campaign-url', views.campaign_url, name='campaign_url'),

    
#    path('scenarios/list-ads-for-segment', views.list_ads_for_segment, name="list_ads_for_segment"),
#    path('scenarios/replace-img-url-segment', views.replace_img_url_segment, name="replace_img_url_segment"),
#    path('scenarios/upload-img-segment', views.upload_img_segment, name="upload_img_segment"),
#    path('scenarios/choose-targeted-segment', views.choose_targeted_segment, name="choose_targeted_segment"),
#    path('scenarios/setup-complete', views.setup_complete_segment, name="setup_complete_segment"),


#    path('content/content-modules/<int:campaign_id>', TemplateView.as_view(template_name='content-modules.html'), name='content-modules'),
#    path('content/content-modules', views.all_content_modules, name='content-modules'),
    path('content/generate-copy/<str:ai_type>/<str:stage>', views.generate_copy, name='generate-copy'),
    path('content/generate-copy/<str:ai_type>', views.generate_copy, name='generate-copy'),
    path('content/generate-copy', views.generate_copy, name='generate-copy'),
    path('content/generate-copy_history/', views.generate_copy_history, name='generate-copy-history'),
#    path('content/update-content-module', views.update_content_module, name='update-content-module'),
#    path('content/content-module-templates', views.content_module_templates, name='content-module-templates'),
#    path('content/media-library/<str:company_code>/dir/', views.get_image_lists_assets_revised.as_view()), # changes #renamed
#    path('content/media-library/<str:company_code>/', views.get_image_lists_assets_revised.as_view(), name="media-library-company-code"), #renamed
#    path('content/media-library', views.get_image_lists_assets_revised.as_view(), name="media-library"), #renamed

#    path('a/content/content-modules/<int:campaign_id>', TemplateView.as_view(template_name='content-modules.html'), name='a-content-modules'),
#    path('a/content/content-modules', TemplateView.as_view(template_name='admin_static/content-modules.html'), name='a-content-modules'),
#    path('a/content/generate-copy/<str:ai_type>', views.generate_copy, name='a-generate-copy'),
#    path('a/content/generate-copy', views.generate_copy, name='a-generate-copy'),
#    path('a/content/content-module-templates', views.content_module_templates, name='a-content-module-templates'),
#    path('a/content/copy-content-modules', views.copy_content_modules, name='a-copy-content-modules'),
#    path('a/content/media-library', TemplateView.as_view(template_name='admin_static/media-library.html'), name='a-media-library'),
 


#    path('analytics/rpt_personalization', TemplateView.as_view(template_name='admin_static/rpt_personalization.html'), name='rpt_personalization'),
#    path('analytics/rpt_funnel', TemplateView.as_view(template_name='admin_static/rpt_funnel.html'), name='rpt_funnel'),
#    path('analytics/rpt_content', TemplateView.as_view(template_name='admin_static/rpt_content.html'), name='rpt_content'),
#    path('analytics/rpt_seo', TemplateView.as_view(template_name='admin_static/rpt_seo.html'), name='rpt_seo'),
#    path('analytics/rpt_page', TemplateView.as_view(template_name='admin_static/rpt_page.html'), name='rpt_page'),
    
#    path('a/analytics/rpt_personalization', TemplateView.as_view(template_name='admin_static/rpt_personalization.html'), name='a-rpt_personalization'),
#    path('a/analytics/rpt_funnel', TemplateView.as_view(template_name='admin_static/rpt_funnel.html'), name='a-rpt_funnel'),
#    path('a/analytics/rpt_content', TemplateView.as_view(template_name='admin_static/rpt_content.html'), name='a-rpt_content'),
#    path('a/analytics/rpt_seo', TemplateView.as_view(template_name='admin_static/rpt_seo.html'), name='a-rpt_seo'),
#    path('a/analytics/rpt_page', TemplateView.as_view(template_name='admin_static/rpt_page.html'), name='a-rpt_page'),
    
#    path('users/users', views.users_listing, name='users'),
#    path('support/faqs', TemplateView.as_view(template_name='admin_static/faqs.html'), name='faqs'),


#    #path('a/scenarios/scenarios', views.scenarios, name='scenarios'),
#    #path('a/scenarios/update-scenario', views.update_scenario),
    
#    #path('a/scenarios/scenarios', views.scenarios, name='scenarios'),
#    #path('a/scenarios/update-scenario', views.update_scenario),
#    path('a/users/users', TemplateView.as_view(template_name='admin_static/users.html'), name='a-users'),
#    path('a/support/faqs', TemplateView.as_view(template_name='admin_static/faqs.html'), name='a-faqs'),


#    path('reports/personalization', TemplateView.as_view(template_name='app/demo/rpt_personalization.html')),
#    path('reports/page', TemplateView.as_view(template_name='app/demo/rpt_page.html')),
#    path('reports/seo', TemplateView.as_view(template_name='app/demo/rpt_seo.html')),
#    path('reports/funnel', TemplateView.as_view(template_name='app/demo/rpt_funnel.html')),
#    path('reports/content', TemplateView.as_view(template_name='app/demo/rpt_content.html')),
#    path('connexus-demo', TemplateView.as_view(template_name='app/connexus-demo.html')),
#    path('client-demo', TemplateView.as_view(template_name='app/client-demo.html')),
#    path('demo', TemplateView.as_view(template_name='app/demo.html')),
#    path('connexus', TemplateView.as_view(template_name='app/connexus.html')),
#    path('bookmarklet', TemplateView.as_view(template_name='app/demo/bookmarklet.html')),
#    path('olb-pre-approved', TemplateView.as_view(template_name='app/demo/olb_bill_pay_add_a_payee.html')),
#    path('olb-bill-pay-enroll', TemplateView.as_view(template_name='app/demo/olb_bill_pay_enroll.html')),
#    path('olb', TemplateView.as_view(template_name='app/demo/account-overview.html')),
#    path('calcoast-geo', TemplateView.as_view(template_name='app/demo/calcoast_geo.html')),
#    path('calcoast-rates', TemplateView.as_view(template_name='app/demo/calcoast_rates.html')),
#    path('calcoast-old-member', TemplateView.as_view(template_name='app/demo/calcoast_old_member.html')),
#    path('calcoast-old', TemplateView.as_view(template_name='app/demo/calcoast_old.html')),
#    path('calcoast-young', TemplateView.as_view(template_name='app/demo/calcoast_young.html')),
#    path('calcoast', TemplateView.as_view(template_name='app/calcoast.html')),
#    path('preview', TemplateView.as_view(template_name='app/preview.html')),
#    path('tag', views.tag),
#    path('campaigns-list', views.campaigns_list, name="campaigns_list"),
#    path('report/campaign/<int:campaign_id>/', views.campaign_report, name="campaign-report"),
#    path('tag', views.tag),    
#    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'),),
#    path(
#        'account/two_factor/setup/complete/',
#        MySetupCompleteView.as_view(),
#        name='setup_complete',
#    ),        
#    path('', include(tf_urls)),
#    path('', include(tf_twilio_urls)),
#    # Override urls
    url(r'^registration/account-email-verification-sent/', views.null_view, name='account_email_verification_sent'),
    url(r'^registration/account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
    url(r'^registration/complete/$', views.complete_view, name='account_confirm_complete'),
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.null_view, name='password_reset_confirm'),

#    #path('login/',
#    #     LoginView.as_view
#    #     (
#    #         template_name='app/login.html',
#    #         authentication_form=forms.BootstrapAuthenticationForm,
#    #         extra_context=
#    #         {
#    #             'title': 'Log in',
#    #             'year' : datetime.now().year,
#    #         }
#    #     ),
#    #     name='login'),
#    path('test_ga_request', views.test_ga_request),
#    path('sf_oauth_callback', views.sf_oauth_callback),
#    path('oauth_callback', views.oauth_callback),
#    path('oauth', views.oauth),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/logout/', LogoutView.as_view(next_page='/'), name='admin_logout'),

#    ## Default urls
    url(r'', include('rest_auth.urls')),
    url(r'^registration/', include('rest_auth.registration.urls')),
#    url(r'session_security/', include('session_security.urls')),

    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
#    path('no-access/', views.no_access, name='no-access'),
#    #path('api-auth/', include('rest_framework.urls')),

    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
#    path('demo_chart/', views.demo_chart),
#    url('^searchableselect/', include('searchableselect.urls')),
#    path('demo_reports', views.demo_reports),
#    path('static', views.static),
#    path('temp', views.temp),
#    path('chart', views.chart_request),
#    #path('growth_rate/', views.growth_rate),
#    path('html', views.static),
#    path('wp-chart', views.wp_example_page),
#    path('combine-chart', views.combine_charts_request),
#    path('refactored-chart', views.render_chart_refactor),
#    path('wp-keywords', views.wp_keyword_sample_page),
#    path('combo-chart', views.combo_chart_request),
#    path('wp', views.wp),
#    path('auth-wp', views.auth_wp),
#    path('rankings', views.rankings),
#    path('auth-rankings', views.auth_rankings),
#    path('analytics', views.analytics2),
#    path('auth-analytics', views.auth_analytics),
#    path('ncua', views.ncua),
#    path('auth-ncua', views.auth_ncua),
#    path('ga', views.ga),
#    path('auth-ga', views.auth_ga),
#    path('ds', views.ds),
#    path('auth-ds', views.auth_ds),
#    path('membership', views.membership),
#    path('auth-membership', views.auth_membership),
#    path('cu_report', views.cu_report),
#    path('auth-cu_report', views.auth_cu_report),
#    path('ptest', views.ptest),
#    path('webhook/<str:endpoint_name>/<str:company_code>', views.webhook),
#    path('images/<str:company_code>/dir/', views.get_image_lists_assets.as_view()), # changes #renamed
#    path('images/<str:company_code>/', views.get_image_lists_assets.as_view()), #renamed
#    path('images/', views.get_image_lists_assets.as_view(), name="media_library"), #renamed    
#    path('command/', views.command_manager),
#    path('qa/<str:company_code>/',  views.qa, name='qa'), #qa    
#    path('qa/', views.qa, name='qa'), #qa
#    path('camera/', TemplateView.as_view(template_name='app/camera.html')),
    path('content/generate_copy_list_data', views.generate_copy_list_data, name='generate_copy_list_data'),
]

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)