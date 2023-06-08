#!/bin/bash
python manage.py dumpdata --indent 2 app.ZipCode > app/fixtures/zipcodes.json
python manage.py dumpdata --indent 2 app.State > app/fixtures/states.json
python manage.py dumpdata --indent 2 app.County > app/fixtures/counties.json
python manage.py dumpdata --indent 2 app.City > app/fixtures/cities.json
python manage.py dumpdata --indent 2 app.GeoTarget > app/fixtures/geotargets.json
