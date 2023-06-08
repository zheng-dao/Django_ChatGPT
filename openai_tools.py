import os
import openai
from django.conf import settings
import time

openai.api_key = settings.OPENAI_KEY
VERSION = 'v1'

def get_endpoint(ai_type='completiond', version=VERSION):
    if version == 'v1':
        endpoints = {
            'chat':'https://api.openai.com/v1/chat/completions',
            'completions':'https://api.openai.com/v1/completions',
            'edits':'https://api.openai.com/v1/edits',
            'images':'https://api.openai.com/v1/images/generations',
            }
    return endpoints.get(ai_type)

def get_template(prompt, ai_type='completions', temperature=1.0, top_p=1.0, max_tokens=75, kwargs=None):
    m = {}
    if ai_type == 'chat':
        m['model'] = "gpt-3.5-turbo"
        m['messages'] = []
        m['messages'].append({'role':'system', 'content':'You are a helpful assistant that writes ad copy.'})
        m['messages'].append({'role':'user', 'content':prompt})
        m['temperature'] = temperature
        m['top_p'] = top_p
        m['max_tokens'] = max_tokens
        # m['stop'] = ["\n"]
    elif ai_type == 'completions':
        m["prompt"] = prompt
        m['model'] = "text-davinci-003"
        m['temperature'] = temperature
        m['max_tokens'] = max_tokens
        m['top_p'] = top_p
        m['frequency_penalty'] = 0.0
        m['presence_penalty'] = 0.0
    elif ai_type == 'edits':
        m["model"] = "text-davinci-edit-001"
        m["input"] = prompt
        # m["instruction"] = "create another option"
        m['temperature'] = temperature
        m['top_p'] = top_p
    elif ai_type == 'images':
        #m["n"] = 1
        m["size"] = "1024x1024"
    if prompt == 'print':
        print(m.keys())
    elif kwargs:
        m = dict(m, **kwargs)
    return m

def create(prompt, ai_type='completions', temperature=1.0, top_p=1.0, max_tokens=75, kwargs=None, version=VERSION):
    response = None
    params = get_template(prompt, ai_type, temperature, top_p, max_tokens, kwargs)
    print('params')
    print(params)
    if version == 'v1':
        if ai_type == 'chat':
            response = openai.ChatCompletion.create(**params)
        elif ai_type == 'completions':
            response = openai.Completion.create(**params)
        elif ai_type == 'edits':
            response = openai.Edit.create(**params)
        elif ai_type == 'images':
            response = openai.Image.create(**params)
    return response

def bulk_create(prompts, ai_type='completions', temperature=1.0, top_p=1.0, max_tokens=75, n=1, sleep=0.5, kwargs=None, version=VERSION):
    responses = []
    if not kwargs:
        kwargs = {}
    kwargs['n'] = n
    for p in prompts:
        responses.append(create(p, ai_type, temperature, top_p, max_tokens, kwargs, version))
        if ai_type == 'edits':
            sleep = 1.0
        time.sleep(sleep)
    return responses
