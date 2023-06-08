from django.core.management.base import BaseCommand, CommandError
from app.models import AnalyticsPlatform, Benchmark, DataSummary, Domain, Keyword, Tier
from django.db.models import Avg, Max, Min, Sum, Count
from timedate import get_qtr
import numpy as np; import pandas as pd

class Command(BaseCommand):
    help = 'do various calculations'

    def add_arguments(self, parser):
        parser.add_argument('calc', nargs='?', type=str)

    def handle(self, *args, **options):
        calc = ['ncua', 'domains', 'keywords', 'digital', 'rankings']
        calc = ['ncua', 'domains', 'digital']
        calc = ['rankings']
        if options['calc']:
            calc = options['calc']

        list_to_calc = ['spam_score', 'domain_authority', 'root_domains_to_root_domain', 'monthly_adwords_budget', 'avg_ad_position', 'organic_domain_ranking', 'paid_domain_ranking', 'organic_clicks_per_month', 'paid_clicks_per_month', 'ppc_value_estimate', 'ppc_clicks_estimate', 'ppc_num_results', 'seo_value_estimate', 'seo_traffic_estimate', 'seo_num_results', 'external_pages_to_root_domain']

        if 'ncua' in calc:
            print('importing ncua data to the domains table')
            ap = AnalyticsPlatform.objects.get(code='ncua')
            domains = Domain.objects.filter(company__company_type='credit_union')
            data_to_get = ['total assets (liabilities, deposits, etc)', 'total number of members', 'total number of loans and leases', 'total amount of loans and leases']
            new_field_names = ['total_assets', 'total_members', 'total_loans', 'total_loans_amount']
            mapping = dict(zip(data_to_get, new_field_names))
            growth_data_to_get = ['total assets (liabilities, deposits, etc)']
            yr = ap.current_year
            qtr = get_qtr(ap.current_qtr)
            dss = DataSummary.objects.filter(series__in=data_to_get, entity_type='credit_union', year=yr, entity_subtype=None)
            dss_co_list = dss.values_list('entity_id', flat=True)
            dssg = DataSummary.objects.filter(series__in=growth_data_to_get, entity_type='credit_union', year=yr, entity_subtype='growth')
            for d in domains:
                if int(d.company.number) in dss_co_list:
                    print(d.name)
                    data = {}
                    for ds in dss.filter(entity_id=d.company.number):
                        data[mapping[ds.series]] = getattr(ds, qtr)
                    gr = dssg.filter(entity_id=d.company.number).first()
                    if gr:
                        data['growth_rate'] = getattr(gr, qtr)
                    d.__dict__.update(**data)
                    d.save()

        if 'digital' in calc:
            print('calculating digital benchmarks')
            tiers = Tier.objects.all().order_by('tier')
            for l in list_to_calc:
                kwargs = {'company__company_type':'credit_union'}
                kwargs[l + '__gt'] = 0
                ap = AnalyticsPlatform.objects.get(code='fin')
                domain_calcs = Domain.objects.filter(**kwargs).aggregate(Min(l), Max(l), Avg(l), Sum(l), Count(l))
                b = {}
                b['ap'] = ap
                b['model_name'] = 'domain'
                b['name'] = l
                b['min'] = domain_calcs[l + '__min']
                b['max'] = domain_calcs[l + '__max']
                b['avg'] = domain_calcs[l + '__avg']
                b['sum'] = domain_calcs[l + '__sum']
                b['count'] = domain_calcs[l + '__count']
                Benchmark.objects.update_or_create(name=l, model_name='domain', ap=ap, benchmark_type=None, defaults=b)

                for j,t in enumerate(tiers):
                    kwargs['asset_tier'] = j+1
                    domain_calcs = Domain.objects.filter(**kwargs).aggregate(Min(l), Max(l), Avg(l), Sum(l), Count(l))
                    b = {}
                    b['ap'] = ap
                    b['model_name'] = 'domain'
                    b['name'] = l
                    b['benchmark_type'] = 'tier'
                    b['benchmark_type_id'] = j+1
                    b['min'] = domain_calcs[l + '__min']
                    b['max'] = domain_calcs[l + '__max']
                    b['avg'] = domain_calcs[l + '__avg']
                    b['sum'] = domain_calcs[l + '__sum']
                    b['count'] = domain_calcs[l + '__count']
                    Benchmark.objects.update_or_create(name=l, model_name='domain', ap=ap, benchmark_type='tier', benchmark_type_id=str(j+1), defaults=b)

        if 'domains' in calc:
            domains = Domain.objects.filter(company__company_type='credit_union', total_assets__gt=0)
            domain_calcs = Domain.objects.filter(company__company_type='credit_union', total_assets__gt=0).aggregate(Min('total_assets'), Max('total_assets'), Avg('total_assets'), Sum('total_assets'), Count('total_assets'), Min('total_members'), Max('total_members'), Avg('total_members'), Sum('total_members'), Count('total_members'), Min('domain_authority'), Max('domain_authority'), Avg('domain_authority'), Sum('domain_authority'), Count('domain_authority'))
            da_min = 0; da_max = 100.0
            total_assets_min = domain_calcs['total_assets__min']
            total_assets_max = domain_calcs['total_assets__max']
            total_members_min = domain_calcs['total_members__min']
            total_members_max = domain_calcs['total_members__max']
            for d in domains:
                if d.total_loans:
                    d.avg_loan_amount = d.total_loans_amount/d.total_loans
                total_assets_scaled = (d.total_assets - total_assets_min)/(total_assets_max - total_assets_min)*100
                total_members_scaled = (d.total_members - total_members_min)/(total_members_max - total_members_min)*100
                if d.total_members > 0:
                    d.assets_per_member = d.total_assets/d.total_members
                    d.domain_authority_per_member = d.domain_authority/d.total_members
                if total_assets_scaled > 0:
                    scaled_da_per_asset = d.domain_authority/total_assets_scaled
                if total_members_scaled > 0:
                    scaled_da_per_member = d.domain_authority/total_members_scaled
                    scaled_assets_per_member = total_assets_scaled/total_members_scaled
                d.domain_authority_per_asset = d.domain_authority/d.total_assets
                d.domain_authority_per_asset_scaled = scaled_da_per_asset
                d.domain_authority_per_member_scaled = scaled_da_per_member
                d.total_assets_scaled = total_assets_scaled
                d.total_members_scaled = total_members_scaled
                d.outperform_da_per_asset = scaled_da_per_asset - 1
                d.outperform_da_per_member = scaled_da_per_member - 1
                d.outperform_assets_per_member = scaled_assets_per_member - 1
                d.save()

        if 'rankings' in calc:
            print('starting rankings')
            final_rankings = {}
            for i, l in enumerate(list_to_calc + ['total_assets', 'growth_rate', 'total_members', 'assets_per_member', 'avg_loan_amount']):
                kwargs = {'company__company_type':'credit_union'}
                print(i, l)
                kwargs[l+'__gt'] = 0
                if l == 'spam_score':
                    kwargs[l+'__gt'] = -2
                domains = Domain.objects.values('id', l).filter(**kwargs).order_by('-'+l)
                df = pd.DataFrame(list(domains))
                #if i==0:
                df_rank = df.copy(deep=True)
                ascending = False
                if l == 'spam_score':
                    ascending = True
                    spam_len = len(df_rank)
                rank = df[l].rank(method='min', ascending=ascending)
                df_rank[l+'_rank'] = rank.fillna(len(rank))
                for d in domains:
                    if d['id'] not in final_rankings:
                        final_rankings[d['id']] = {}
                    final_rankings[d['id']].update({l+'_rank':int(df_rank[df_rank['id']==d['id']].fillna(len(df_rank))[l+'_rank'])})
            domains = Domain.objects.filter(company__company_type='credit_union')
            for d in domains:
                if d.spam_score in [-1,0]:
                    d.spam_score_rank = spam_len + 1
                    final_rankings[d.id].update({'spam_score':100})
                if d.id in final_rankings:
                    di, created = Domain.objects.update_or_create(id=d.id, defaults=final_rankings[d.id])

        if 'keywords' in calc:
            keywords = Keyword.objects.all()
            print('Updating keyword values')
            for k in keywords:
                k.ctr_scaled = 0
                k.save()
            kw_calcs = Keyword.objects.filter(rawExactLocalMonthlySearchVolume__gt=0).aggregate(Min('monthly_volume'), Max('monthly_volume'), Avg('monthly_volume'), Sum('monthly_volume'), Count('monthly_volume'), Min('ctr'), Max('ctr'), Avg('ctr'), Sum('ctr'), Count('ctr'), Min('clicks'), Max('clicks'), Avg('clicks'), Sum('clicks'), Count('clicks'))
            print('Calculating keyword estimates')
            for k in keywords:
                if k.monthly_volume > 0:
                    k.monthly_volume_scaled = (k.monthly_volume - kw_calcs['monthly_volume__min'])/(kw_calcs['monthly_volume__max'] - kw_calcs['monthly_volume__min'])*100
                    k.clicks_scaled = (k.clicks - kw_calcs['clicks__min'])/(kw_calcs['clicks__max'] - kw_calcs['clicks__min'])*100
                    k.ctr_scaled = (k.ctr - kw_calcs['ctr__min'])/(kw_calcs['ctr__max'] - kw_calcs['ctr__min'])*100
                    k.save()


