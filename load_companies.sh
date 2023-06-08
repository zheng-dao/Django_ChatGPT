#!/bin/bash
python manage.py loaddata app/fixtures/companies.json
python manage.py loaddata app/fixtures/domains.json
python manage.py loaddata app/fixtures/competitors.json
#python manage.py loaddata app/fixtures/revenuekpis.json
python manage.py loaddata app/fixtures/urlpatterns.json
