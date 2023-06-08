from django.core.management.base import BaseCommand
from app.models import GlobalSetting
from app.signals.handlers import write_pconfig

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-co', nargs='+', type=str)

    def handle(self, *args, **options):
        print(options)
        co = options['co'][0]
        gs = GlobalSetting.objects.filter(company__code=co).first()
        write_pconfig(gs)

        