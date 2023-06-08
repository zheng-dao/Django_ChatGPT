#!/bin/bash
python -Xutf8 manage.py dumpdata --indent 2 app.GlobalSetting > app/fixtures/globalsettings.json