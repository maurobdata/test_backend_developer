#! /bin/sh

file=django_rest_app/app_rest/db.sqlite3
if [ -e "$file" ]; then
  # Control will enter here if $file exists
  rm $file
fi

# User credentials
user=admin
email=admin@example.com
password=admin

python3 django_rest_app/app_rest/manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('$user', '$email', '$password')" | python3 django_rest_app/app_rest/manage.py shell
