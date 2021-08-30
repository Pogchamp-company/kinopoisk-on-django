source env.sh
source venv/bin/activate
cd src
python manage.py migrate
python manage.py collectstatic
