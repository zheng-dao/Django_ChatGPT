call python manage.py dumpdata --indent 2 app.ParentKeyword > app/fixtures/parentkeywords.json
call python manage.py dumpdata --indent 2 app.Keyword > app/fixtures/keywords.json
call python manage.py dumpdata --indent 2 app.KeywordGroup > app/fixtures/keywordgroups.json
::call python manage.py dumpdata --indent 2 app.Page > app/fixtures/pages.json
::call python manage.py dumpdata --indent 2 app.PageKeyword > app/fixtures/pagekeywords.json
::call python manage.py dumpdata --indent 2 app.DomainKeywordGroup > app/fixtures/domainkeywordgroups.json
