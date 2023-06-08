call python manage.py dumpdata --indent 2 app.Company > app/fixtures/companies.json
call python manage.py dumpdata --indent 2 app.Domain > app/fixtures/domains.json
call python manage.py dumpdata --indent 2 app.Competitor > app/fixtures/competitors.json
::call python manage.py dumpdata --indent 2 app.RevenueKPI > app/fixtures/revenuekpis.json
call python manage.py dumpdata --indent 2 app.UrlPattern > app/fixtures/urlpatterns.json
