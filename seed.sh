cd parser
wget https://github.com/Pogchamp-company/kinopoisk_on_django/releases/download/v0.2-beta/movies.json
wget https://github.com/Pogchamp-company/kinopoisk_on_django/releases/download/v0.2-beta/persons.json
wget https://github.com/Pogchamp-company/kinopoisk_on_django/releases/download/v0.2-beta/assets.zip
unzip assets.zip
python formatter.py
cd ..
python manage.py shell -c 'from movies.models import Movie;Movie.objects.all().delete()'
manage.py loaddata seed/movies.json
manage.py loaddata seed/persons.json
manage.py load_posters
manage.py load_photos
manage.py seed_users 10000
manage.py seed_scores