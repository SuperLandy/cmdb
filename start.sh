cd /opt/cmdb/
python manage.py makemigrations
python manage.py migrate
nohup python manage.py runserver 0.0.0.0:80 --insecure 1>/dev/null 2>/dev/null &
