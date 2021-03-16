#!/bin/bash

sudo su

cd /var/www/airbnb_project/

echo "Install requirements..."
. /var/www/airbnb_project/venv/bin/activate

pip install -r /var/www/airbnb_project/requirements.txt
python3 manage.py migrate

echo "Main service reload..."
sudo systemctl restart nginx
sudo systemctl restart gunicorn

# echo "Celery reload..."
# cp -f /var/www/rainwalk/api/scripts/celery-worker.conf /etc/supervisor/conf.d/
# supervisorctl reload
