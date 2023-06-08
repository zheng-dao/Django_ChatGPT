import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ga.settings")
import django
django.setup()

from locust import HttpUser, task
import json
from django.conf import settings
from rest_framework.authtoken.models import Token


#https://finalyticsdata.com
#https://stgfinalyticsdata.com
#http://localhost:8000
#http://localhost:8001

#class ApiPost(HttpUser):
#    @task
#    def hello_world(self):
#        #urltotest = 'https://stgfinalyticsdata.com'
#        #if settings.ENV == 'prod':
#        #    urltotest = 'https://finalyticsdata.com'
#        urltotest = self.host
#        urltotest += '/api/v1/ads'
#        token  = settings.FIN_API_TOKEN
#        headers = {'Authorization':'Token ' + token}
#        data = {'payload':{'cu_id':'68490', 'page':'/'}, 'is_encrypted':False}
        
#        #self.client.get("/api/v1/ads?cu_id=68490")
#        r = self.client.post(urltotest, json=data, headers=headers, name='Test 1')
#        #print(json.loads(r.text))

class PageGet(HttpUser):
    @task
    def hello_world(self):
        urltotest = self.host
        self.client.get(urltotest)
        #r = self.client.post(urltotest, json=data, headers=headers, name='Test 1')
        #print(json.loads(r.text))
