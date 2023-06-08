'''
This is for importing the keyword data for testing
'''

from app.models import Keyword
from django.core.management.base import BaseCommand
import random


class Command(BaseCommand):
    help = "help to import random number from 1-100"

    keywords_filter = Keyword.objects.filter(is_location=True)


    for key_ in keywords_filter:
        key_.rawExactLocalMonthlySearchVolume = random.choice(range(0,99))
        key_.rawPhraseLocalMonthlySearchVolume = random.choice(range(0,99))

        key_.save()

        print(key_)
        

