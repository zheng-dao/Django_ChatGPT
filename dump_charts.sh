#!/bin/bash
python manage.py dumpdata --indent 2 app.AnalyticsPlatform > app/fixtures/analyticsplatforms.json
python manage.py dumpdata --indent 2 app.Metric > app/fixtures/metrics.json
python manage.py dumpdata --indent 2 app.Sheet > app/fixtures/sheets.json
python manage.py dumpdata --indent 2 app.ChartStyle > app/fixtures/chartstyles.json
python manage.py dumpdata --indent 2 app.ChartType > app/fixtures/charttypes.json
python manage.py dumpdata --indent 2 app.Chart > app/fixtures/charts.json
python manage.py dumpdata --indent 2 app.Report > app/fixtures/reports.json
python manage.py dumpdata --indent 2 app.MultiReport > app/fixtures/multireports.json
