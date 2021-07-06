release: python django_rest_app/app_rest/manage.py makemigrations --no-input
release: python django_rest_app/app_rest/manage.py migrate --no-input

web: gunicorn --pythonpath django_rest_app/app_rest app_rest.wsgi