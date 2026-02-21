release: ./manage.py migrate --no-input && ./initialdata.sh

web: gunicorn --config gunicorn.conf.py core.wsgi
 