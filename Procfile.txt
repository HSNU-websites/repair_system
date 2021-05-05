release: python manage.py reset -y
web: gunicorn manage:app