from django.apps import AppConfig
from django.core.cache import cache

class AppSigsConfig(AppConfig):
    name = 'app'
    verbose_name = "App"

    def ready(self):
        import app.signals.handlers #noqa
    #    #import allauth.account.signals
    #    #import os
    #    #from file_tools import load_json
    #    #from django.conf import settings

    #    #PCONFIG = {}
    #    ##for code in CO_CODES:
    #    #try:
    #    #    code = 'vys'
    #    #    folder = settings.ENV
    #    #    fp = os.path.join('app/model_files', code, folder)
    #    #    if os.path.exists(fp):
    #    #        j = load_json('pconfig.json', fp=fp)
    #    #        if j:
    #    #            PCONFIG[code] = j
    #    #    else:
    #    #        print('pconfig path does not exist for ', code)
    #    #        #lg.info(('pconfig path does not exist for ', code))
    #    #except Exception as e:
    #    #    print('There was an error importing pconfig.json for ', code)
    #    #    print(str(e))
    #    #    #lg.info(('There was an error importing pconfig.json for ', code))
    #    #    #lg.info(str(e))
    #    #cache.set('PCONFIG', PCONFIG)
    #    #print(cache.get(PCONFIG), 'apps')
