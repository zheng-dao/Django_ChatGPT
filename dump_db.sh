#!/bin/bash
call python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 > app/fixtures/db.json