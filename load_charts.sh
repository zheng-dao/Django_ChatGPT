#!/bin/bash
python manage.py loaddata app/fixtures/analyticsplatforms.json
python manage.py loaddata app/fixtures/metrics.json
python manage.py loaddata app/fixtures/sheets.json
python manage.py loaddata app/fixtures/chartstyles.json
python manage.py loaddata app/fixtures/charttypes.json
python manage.py loaddata app/fixtures/charts.json
python manage.py loaddata app/fixtures/reports.json
python manage.py loaddata app/fixtures/multireports.json
