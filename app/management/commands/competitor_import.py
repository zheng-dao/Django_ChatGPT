from django.core.management.base import BaseCommand
from app.models import Competitor, Company, Domain
import spyfu_tools
from spyfu_tools import get_competitors

class Command(BaseCommand):
    help = 'import competitors for a single credit union (or all of them)'

    def add_arguments(self, parser):
        parser.add_argument('domain_name', nargs='?', type=str, default='clients')

    def handle(self, *args, **options):
        print(options)
        domain_name = options['domain_name']
        domains = Domain.objects.filter(name=domain_name)
        if domain_name == 'clients':
            domains = Domain.objects.filter(company__is_client=True)
        if domain_name == 'subscribers':
            domains = Domain.objects.filter(company__is_subscriber=True)

        for domain in domains:
            #try:
                print(domain)
                competitors = spyfu_tools.call_api(domain.name, call_type='get_domain_competitors_us', api='core_api', extras={'isOrganic':'true', 'r':'10'})
                #competitors_list = [c['domainName'] for c in competitors]
                #domain_co_list = Domain().is_cu(competitors_list)
                competitors = Competitor().save_competitors(domain.company, competitors)
                print(competitors)
                print('-----------------------')
            #except Exception as e:
                #print('ERROR******************')
                #print(e)

