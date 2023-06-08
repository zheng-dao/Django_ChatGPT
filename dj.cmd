@ECHO OFF
if %1%==run (
cmd /k "python manage.py runserver"
)
if %1%==sh (
::cmd /k "python manage.py shell"
python manage.py shell
)
if %1%==mkmig (
cmd /k "python manage.py makemigrations app"
)
if %1%==mig (
cmd /k "python manage.py migrate app"
)
if %1%==pm (
set pm_cmd="python manage.py pmrunall -c "%2% 
cmd /k %pm_cmd%
)
if %1%==dump (
set mdl=%2%
::set dump_cmd="python -Xutf8 manage.py dumpdata --indent 2 app.%mdl% > app/fixtures/%mdl%s.json"
cmd /k "python -Xutf8 manage.py dumpdata --indent 2 app.%mdl% > app/fixtures/%mdl%s.json"
)
if %1%==load (
set mdl=%2%
cmd /k "python manage.py loaddata app/fixtures/%mdl%s.json"
)
if %1%==m (
set mg="python manage.py "%2%
cmd /k %mg%
)

