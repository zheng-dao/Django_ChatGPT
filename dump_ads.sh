#!/bin/bash
python manage.py dumpdata --indent 2 app.Campaign > app/fixtures/campaigns.json
python -Xutf8 manage.py dumpdata --indent 2 app.AdCopy > app/fixtures/adcopy.json
python -Xutf8 manage.py dumpdata --indent 2 app.AdTemplate > app/fixtures/adtemplates.json
python -Xutf8 manage.py dumpdata --indent 2 app.Ad > app/fixtures/ads.json
python -Xutf8 manage.py dumpdata --indent 2 app.Asset > app/fixtures/assets.json
python -Xutf8 manage.py dumpdata --indent 2 app.TestScenario > app/fixtures/testscenarios.json
