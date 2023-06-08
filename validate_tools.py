import numpy as np
from django.conf import settings

DATA_TYPES = {
    'is_encrypted':bool,
    'timestamp':int,
    }
PAYLOAD_KEYS = [
    'cu_id',
    'demographics.segments.firsttime.timestamp',
    'demographics.zipcode',
    'device.form_factor',
    'last.location.zip',
    'last.referrer',
    'last_product_url',
    'org',
    'original_referring_url',
    'referrer',
    'zipcode',
    ]
PAYLOAD_ERROR_KEYS = [
    'payload',
    ]
FUNNEL_KEYS = [
    'demographics.segments.firsttime.timestamp',
    'demographics.applications.started',
]
REFERRER_KEYS = {
    'landing_page':{},
    'timestamp':{'data_type':int},
    'url':{},
    'utm':{'data_type':dict},
    'utm.utm_term':{},
}
SEARCH_KEYS = [
    'category',
    'term',
    'timestamp',
]
ZIPCODE_KEYS = [
    'demographics.zip',
    'last.location.zipcode',
    'zipcode',
]
REQUIRED_KEYS = {}
REQUIRED_KEYS['root'] = {
    'is_encrypted':{'data_type':bool},
    'payload':{},
}
REQUIRED_KEYS['funnel'] = FUNNEL_KEYS
REQUIRED_KEYS['last'] = {}
REQUIRED_KEYS['last']['referrer'] = REFERRER_KEYS
REQUIRED_KEYS['last']['search'] = SEARCH_KEYS
REQUIRED_KEYS['last']['url'] = {
    'product.category':{},
    'product.timestamp':{'data_type':int},
    'product.url':{},
    'product.url_type':{'value':'product'},
}
REQUIRED_KEYS['org'] = ['org']
REQUIRED_KEYS['payload'] = PAYLOAD_KEYS
REQUIRED_KEYS['payload_error'] = PAYLOAD_ERROR_KEYS
REQUIRED_KEYS['products_owned'] = ['products_owned']
REQUIRED_KEYS['products_default'] = ['products_owned']
REQUIRED_KEYS['segment'] = ['demographics.segments']
REQUIRED_KEYS['transaction'] = ['demographics.transactions']
REQUIRED_KEYS['zipcode'] = ZIPCODE_KEYS

#			"product": {
#				"attributes": null,
#				"audience": [
#					"[]"
#				],
#				"category": "car loan",
#				"is_app_complete": false,
#				"is_app_start": false,
#				"is_dynamic": false,
#				"is_reviewed": true,
#				"platform_mode": null,
#				"subcategory": null,
#				"timestamp": 1674175438538,
#				"url": "/autoloans",
#				"url_type": "product"
#			},

#segment
#referrer
#search
#url
#transaction
#funnel
#org
#ftv (first time visitor)
#distance
#products_owned
#zipcode
#products_default

def remove_keys(keys_to_remove, keys):
    if isinstance(keys, dict):
        for key in keys_to_remove:
            skey_list = key.split('.')
            temp_dict = keys[skey_list[0]]
            skey_len = len(skey_list)
            for i,skey in enumerate(skey_list):
                if i == skey_len - 1:
                    temp_dict.pop(skey, None)
                else:
                    temp_dict = temp_dict[skey]
    elif isinstance(keys, list):
        keys = list(set(keys) - set(keys_to_remove))
    return keys

def get_required_keys(category='payload', session_init=False, keys=[], return_list=True):
    if not keys:
        keys = REQUIRED_KEYS[category]

    if category == 'payload':
        if session_init:
            print('session init keys removed')
            list_to_remove = ['demographics.zip', 'last.location.zipcode', 'org', 'zipcode']
            keys = remove_keys(list_to_remove, keys)

    if return_list and isinstance(keys, dict):
        keys = list(keys.keys())
    return keys

def check_all_good(all_good):
    return np.all([True if x is True else False for x in all_good])

def testit(value, data, test='in', test_value_present=True):
    is_good = False
    if test == 'in':
        if value == '*':
            is_good = True
        else:
            if value in data:
                is_good = True
            else:
                is_good = {'value':value, 'data':'', 'error':'The value was not in the iterable'}
    if test_value_present and is_good == True:
        val = data.get(value)
        if not val and not val == False:
            is_good = {'value':value, 'data':data, 'error':'The value was not present'}
    return is_good

def testits(subkeys, data, test='in'):
    errors=[]
    keylist = subkeys
    if isinstance(subkeys, str):
        keylist = subkeys.split('.')
    all_good = [False]*len(keylist)
    last_key_good = False
    for i,key in enumerate(keylist):
        #print(i, key)
        #print(data.keys())
        if len(keylist) == 1:
            return testit(keylist[i], data, test)
        else:
            if i == 0 or last_key_good == True:
                if i != 0:
                    data = data[keylist[i-1]]
                errors.append(testits([keylist[i]], data, test))
                last_key_good = errors[-1]
    if i == len(keylist) - 1:
        all_good = check_all_good(errors)
        if all_good == True:
            return True
    return errors

def test_data_type(key, reqs, data):
    is_good = False
    if isinstance(reqs, dict):
        data_type = reqs.get('data_type')
        if data_type:
            if isinstance(data.get(key), data_type):
                is_good = True
        else:
            is_good = True
    else:
        is_good = True
    return is_good

def validate_getads_post(post, algorithms, session_init=False, only_return_errors=False):
    all_good = False
    errors = {}

    root_keys = get_required_keys('root', session_init, return_list=False)
    for root_key in root_keys.keys():
        print('root', root_key)
        errors['root keys required: ' + root_key] = testit(root_key, post)
        errors['root keys values: ' + root_key] = test_data_type(root_key, root_keys.get(root_key), post)
    print('root', errors)
    print('------------------------------------')
    
    payload = post.get('payload')
    if payload:
        for key in get_required_keys('payload', session_init):
            print('payload', key)
            errors['keys required: payload'] = testits(key, payload, 'in')
        print('payload', errors)
        print('------------------------------------')

        if payload.get('page') == '/olb/account-details':
            required_keys = get_required_keys('transaction', session_init)
            for rkey in required_keys:
                print('rkey', rkey)
                errors['keys required: ' + key + ' ' + rkey] = testits(rkey, payload, 'in')

        for key, value in algorithms.items():
            if key not in settings.LAST_ALGORITHMS:
                print('not last', key.upper())
                required_keys = get_required_keys(key, session_init)
                for rkey in required_keys:
                    print('rkey', rkey)
                    errors['keys required: ' + key + ' ' + rkey] = testits(rkey, payload, 'in')
        print('not last', errors)
        print('------------------------------------')

        last = payload.get('last')
        if last:
            for key, value in algorithms.items():
                if key in settings.LAST_ALGORITHMS:
                    print('last', key.upper())
                    required_keys = get_required_keys('last', session_init, return_list=False)
                    required_keys = required_keys.get(key)
                    if required_keys:
                        for lkey in required_keys:
                            if key != 'url':
                                lkey = key + '.' + lkey
                            print('lkey', lkey)
                            errors['keys required: last - ' + lkey] = testits(lkey, last, 'in')
                    else:
                        errors['"last" key not present: ' + key] = {'value':'last.' + key, 'data':None, 'error':'Required fields have not been input for this algorithm, yet'}
            print('last', errors)
            print('------------------------------------')

        else:
            errors['"last" key not present'] = {'value':'last', 'data':'', 'error':'The key was not present'}
    else:
        errors['payload key not present'] = {'value':'payload', 'data':'', 'error':'The key was not present'}

    all_good = check_all_good(errors.values())
    if all_good:
        return True
    if only_return_errors:
        final_errors = {}
        for k,v in errors.items():
            if not v == True:
                final_errors[k] = v
        return final_errors
    return errors





#Payload Required: Session Init
#- tbd

#Payload Required: After Session Init
#- zipcode
#-- demographics.zip
#-- last.location.zipcode
#- org

#Product Page Visits
#- if the user visits any product page during ANY session that has a page.category OR the response payload contained a data.page.category then last.product.category is required
#-- last_product_url: required

#Segment Page Visits
#- if the user visits any page during ANY session that has a page.audience demographics.segments.[name of segment].timestamp is required

#Search
#- if a search has been run during ANY session then last.search.term is required
#-- last.search.category should also persist if the autocategorizer returns a category for the search term

#External Referrer (ie not from within the CU's domain or any of its subdomains)
#- last.referrer.url required
#- last.referrer.landing_page required
#-- if utm parameters
#--- utm dict should be populated with data from all of the utm parameters
#-- all this data should persist in last.referrer until another external URL refers and is detected (ie no logged as None or noreferrer)

#If OLB client:
#- products_owned required if the user visits the account summary page for a client with OLB activated (ie finalytics cookie was populated with products_owned)


#{
#	"is_encrypted": false,
#	"payload": {
#		"actions": {},
#		"alert_cookies": {},
#		"cu_id": "17429",
#		"demographics": {
#			"segments": {
#				"firsttime": {
#					"timestamp": 1674174633387
#				}
#			},
#			"zip": ""
#		},
#		"device": {
#			"date": "2023-01-20T00:31:05.097Z",
#			"form_factor": "desktop",
#			"height": 919,
#			"name": "firefox",
#			"os": "Windows 10",
#			"type": "browser",
#			"ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
#			"version": "109.0.0",
#			"width": 1332
#		},
#		"devices": {
#			"date": "2023-01-20T00:30:32.870Z",
#			"form_factor": "desktop",
#			"height": 895,
#			"name": "firefox",
#			"os": "Windows 10",
#			"type": "browser",
#			"ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
#			"version": "109.0.0",
#			"width": 1479
#		},
#		"host_env": "prod",
#		"id": "c908733d-22ab-47f7-8d60-a4cd429528f4",
#		"ip": "",
#		"last": {
#			"device": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
#			"location": {},
#			"login": null,
#			"oao": null,
#			"page": {
#				"path": "/",
#				"timestamp": 1674174634254
#			},
#			"pageview": "https://visionsfcu.org",
#			"product": {
#				"attributes": null,
#				"audience": [
#					"[]"
#				],
#				"category": "car loan",
#				"is_app_complete": false,
#				"is_app_start": false,
#				"is_dynamic": false,
#				"is_reviewed": true,
#				"platform_mode": null,
#				"subcategory": null,
#				"timestamp": 1674175438538,
#				"url": "/autoloans",
#				"url_type": "product"
#			},
#			"referrer": {
#				"landing_page": "https://www.finalyticsdemo.com/?utm_source=google&ut_medium=banner&utm_campaign=FSU_Loyalty&utm_term=fsu",
#				"name": "Easterly Financial | Banking with the Best",
#				"timestamp": 1674177672617,
#				"title": "Easterly Financial | Banking with the Best",
#				"url": "https://www.finalyticsdemo.com/",
#				"utm": {
#					"utm_campaign": "FSU_Loyalty",
#					"utm_source": "google",
#					"utm_term": "fsu"
#				}
#			},
#			"search": {
#				"term": "car loan",
#				"timestamp": 1674177169498,
#				"url": "q=car+loan&scpage=1&scupdated=1&scorder=_score"
#			},
#			"session": {
#				"2023-01-19": {
#					"end": 0,
#					"start": 1674174634253
#				}
#			}
#		},
#		"last_product_url": "",
#		"locations": [
#			{
#				"ips": "",
#				"latlongs": [
#					0,
#					0
#				],
#				"timestamp": 1674174634254,
#				"zips": ""
#			}
#		],
#		"log": {},
#		"mode": "revenue_per_member",
#		"models": "",
#		"org": "AT&T U-verse",
#		"original_referring_url": "https://visionsfcu.org/",
#		"page": "/",
#		"pdp": null,
#		"products_owned": "",
#		"products_recommended": "",
#		"referrer": "https://visionsfcu.org/?cb=1",
#		"suppress": "",
#		"use_distance_model": "",
#		"visits": {
#			"2023-01-19": {
#				"end": 1674174662263,
#				"start": 1674174634254
#			}
#		},
#		"zipcode": "94941"
#	}
#}