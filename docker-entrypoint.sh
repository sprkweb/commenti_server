#!/bin/sh

if ! pipenv run ./manage.py migrate --check --noinput; then
    echo
    echo "Unapplied migrations are detected. Migrating..."
    pipenv run ./manage.py migrate --noinput
fi

cat <<EOF | pipenv run ./manage.py shell
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="$DJANGO_SUPERUSER_USERNAME").exists():
    print("Creating superuser...")
    User.objects.create_superuser(username="$DJANGO_SUPERUSER_USERNAME", password="$DJANGO_SUPERUSER_PASSWORD")
EOF

exec "$@"
