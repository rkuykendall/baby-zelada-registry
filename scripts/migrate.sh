source venv/bin/activate
heroku pg:backups:capture --app baby-zelada-registry
python manage.py makemigrations
python manage.py migrate
.