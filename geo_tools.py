import os, json
import csv
from django.conf import settings
from file_tools import map_fields, load_csv_data, get_list_indices, map_fields_for_data_summary
from app.models import AnalyticsPlatform, Company, Domain, DataSummary, Ip, Location, Tier
from datetime import date
from timedate import get_qtr
import time
from django.core.management import call_command
import copy
from bs4 import BeautifulSoup
import requests
import geoip2.webservice
from geopy.distance import great_circle
from django.core.mail import send_mail

PLATFORM_CODE = 'geoip'
SLEEP = 1

#https://positionstack.com/documentation
def get_lat_long(loc):
    url = 'http://api.positionstack.com/v1/forward'
    url += '?access_key=' + settings.POSITION_STACK_KEY
    url += '&query=' + loc.physicaladdressline1 + ', ' + loc.physicaladdresscity + ', ' + loc.physicaladdressstatecode + ' ' + loc.physicaladdresspostalcode
    r = requests.get(url)
    if r.status_code == 200:
        try:
            data = json.loads(r.text)
            return data['data'][0]['latitude'], data['data'][0]['longitude']
        except Exception as e:
            print(e, r.text)
            return None, None

def get_all_lat_long(locs=None):
    if not locs:
        locs = Location.objects.filter(latitude=None)
    for i, loc in enumerate(locs):
        lat, lon = get_lat_long(loc)
        if lat and lon:
            loc.latitude = lat
            loc.longitude = lon
            loc.save()
        else:
            print(i)
        time.sleep(SLEEP)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def visitor_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_geo_data(ip, saveit=True, api_type='city', company=None):
    data = {}
    try:
        client = geoip2.webservice.Client(settings.GEOIP_ACCOUNT_ID, settings.GEOIP_KEY)
        if api_type == 'city':
            g = client.city(ip)
        elif api_type == 'insights':
            g = client.insights(ip)
        elif api_type == 'country':
            g = client.country(ip)
        if g:
            data['zipcode'] = g.postal.code
            data['geoname_id'] = g.city.geoname_id
            data['ip'] = ip
            data['city'] = g.city.name
            data['state'] = g.subdivisions.most_specific.iso_code
            data['country'] = g.country.name
            data['metro_code'] = g.location.metro_code
            data['latitude'] = g.location.latitude
            data['longitude'] = g.location.longitude
            data['isp'] = g.traits.isp
            data['organization'] = g.traits.organization
            data['network'] = g.traits.network
            data['timezone'] = g.location.time_zone
            if company:
                data['company'] = company
        if saveit:
            ip = Ip.objects.update_or_create(ip=ip, defaults=data)
        #data = {'ip':ip}
        data.pop('network', None)
        data.pop('company', None)
    except Exception as e:
        if not ip.startswith(('10.', '192.168.', '172.16.', '172.17.', '172.18.', '172.19.', '172.20.', '172.21.', '172.22.', '172.23.', '172.24.', '172.25.', '172.26.', '172.27.', '172.28.', '172.29.', '172.30.', '172.31.')):
           send_mail('GEO API Call Failed: ' + str(date.today()), str(e), settings.DEFAULT_FROM_EMAIL, settings.NOTIFICATIONS['admins'])
    return data

def get_distance(a, b):
    distance = great_circle(a, b).miles
    return distance

def get_county(lat, lon, return_county=True, return_state=True, format='json'):
    url = 'https://geo.fcc.gov/api/census/area'
    full_url = ('%s?lat=%s&lon=%s&format=%s')%(url, lat, lon, format)
    r = requests.get(full_url)
    if r.status_code == 200:
        j = json.loads(r.text)
        if 'results' in j and len(j['results']) > 0:
            if return_county and return_state:
                return j['results'][0]['county_name'] + ' County, ' + j['results'][0]['state_name']
            elif return_county:
                return j['results'][0]['county_name']
            elif return_state:
                j['results'][0]['state_name']
            else:
                return j['results'][0]
    return {}