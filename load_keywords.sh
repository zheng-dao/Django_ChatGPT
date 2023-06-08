#!/bin/bash
python manage.py loaddata app/fixtures/parentkeywords.json
python manage.py loaddata app/fixtures/keywords.json
python manage.py loaddata app/fixtures/keywordgroups.json
#python manage.py loaddata app/fixtures/pages.json
#python manage.py loaddata app/fixtures/pagekeywords.json
#python manage.py loaddata app/fixtures/domainkeywordgroups.json
