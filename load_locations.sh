#!/bin/bash
python manage.py loaddata app/fixtures/zipcodes.json
python manage.py loaddata app/fixtures/states.json
python manage.py loaddata app/fixtures/counties.json
python manage.py loaddata app/fixtures/cities.json
python manage.py loaddata app/fixtures/geotargets.json
