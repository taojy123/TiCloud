#!/bin/bash

appname=ti;

mkdir -p  /var/data;

echo $appname;

if [[ -z "$1" ]]; then
    echo "run server";
    python manage.py migrate;
    python manage.py collectstatic --noinput;
    gunicorn -k gevent -w 5 -b 0.0.0.0:8000 --error-logfile=- --access-logfile=- $appname.wsgi;
elif [[ "$1" = "worker" ]]; then
    echo "run celery worker";
    celery worker -A $appname -l info;
elif [[ "$1" = "beat" ]]; then
    echo "run celery beat";
    celery beat -A $appname -l info;
elif [[ "$1" = "flower" ]]; then
    echo "run celery flower";
    flower -A $appname --address=0.0.0.0 --db=/var/data/flower.db --persistent=True;
else
    echo "$@"
    exec "$@"
fi
