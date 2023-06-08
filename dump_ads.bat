call python manage.py dumpdata --indent 2 app.Campaign > app/fixtures/campaigns.json
call python -Xutf8 manage.py dumpdata --indent 2 app.AdCopy > app/fixtures/adcopy.json
call python -Xutf8 manage.py dumpdata --indent 2 app.AdTemplate > app/fixtures/adtemplates.json
call python -Xutf8 manage.py dumpdata --indent 2 app.Ad > app/fixtures/ads.json
call python -Xutf8 manage.py dumpdata --indent 2 app.Asset > app/fixtures/assets.json
call python -Xutf8 manage.py dumpdata --indent 2 app.TestScenario > app/fixtures/testscenarios.json
call python -Xutf8 manage.py dumpdata --indent 2 app.faqquestion > app/fixtures/faqquestions.json
call python -Xutf8 manage.py dumpdata --indent 2 app.faqanswer > app/fixtures/faqanswers.json
call python -Xutf8 manage.py dumpdata --indent 2 app.offer > app/fixtures/offers.json
