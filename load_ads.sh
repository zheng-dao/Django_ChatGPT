#!/bin/bash
python manage.py loaddata app/fixtures/campaigns.json
python manage.py loaddata app/fixtures/adcopy.json
python manage.py loaddata app/fixtures/adtemplates.json
python manage.py loaddata app/fixtures/ads.json
python manage.py loaddata app/fixtures/assets.json
python manage.py loaddata app/fixtures/testscenarios.json