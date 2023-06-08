call python manage.py dumpdata --indent 2 app.AnalyticsPlatform > app/fixtures/analyticsplatforms.json
call python manage.py dumpdata --indent 2 app.Metric > app/fixtures/metrics.json
call python manage.py dumpdata --indent 2 app.Sheet > app/fixtures/sheets.json
call python manage.py dumpdata --indent 2 app.ChartStyle > app/fixtures/chartstyles.json
call python manage.py dumpdata --indent 2 app.ChartType > app/fixtures/charttypes.json
call python manage.py dumpdata --indent 2 app.Chart > app/fixtures/charts.json
call python manage.py dumpdata --indent 2 app.Report > app/fixtures/reports.json
call python manage.py dumpdata --indent 2 app.MultiReport > app/fixtures/multireports.json
