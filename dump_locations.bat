call python manage.py dumpdata --indent 2 app.ZipCode > app/fixtures/zipcodes.json
call python manage.py dumpdata --indent 2 app.State > app/fixtures/states.json
call python manage.py dumpdata --indent 2 app.County > app/fixtures/counties.json
call python manage.py dumpdata --indent 2 app.City > app/fixtures/cities.json
call python manage.py dumpdata --indent 2 app.GeoTarget > app/fixtures/geotargets.json
