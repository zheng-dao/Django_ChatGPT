from django.core.management.base import BaseCommand
from app.models import Page, Domain
class Command(BaseCommand):
    
    def handle(self, *args, **options):
        pages_instances = Page.objects.filter(domain=None)
        for page_instance in pages_instances:
            print(page_instance.url)
            domain_instance = Domain().get_domain(page_instance.url, instance=True)
            if domain_instance:
                page_instance.domain = domain_instance
                page_instance.save()
                print(f"Domain is saved for ", page_instance.url)
            else:
                print(f'Domain instance is not found for {page_instance.url}')
