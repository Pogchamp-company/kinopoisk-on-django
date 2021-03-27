from os import getenv
from kinopoisk_api import KP
import time

from src.parser.utils import load_json, save_json

kinopoisk = KP(token=getenv('KP_API_KEY'))


top250 = kinopoisk.top250()
try:
    top_movies = load_json('movies.json')
except:
    top_movies = []
try:
    persons = load_json('persons.json')
except:
    persons = []

for item in top250:
    start = time.time()
    print(item.name)
    full_info = kinopoisk.get_film(item.kp_id)
    movie = {
        "title": item.ru_name,
        "original_title": item.name,
        "movie_type": 2,  # Фильм
        "year": item.year,
        "slogan": full_info.tagline,
        "description": full_info.description,
        "duration": item.duration + ":00",
        "premiere": full_info.premiere,
        "premiere_ru": full_info.premiere_ru,
        "rating_mpaa": full_info.mpaa_rating,
        "age_rating": full_info.age_rating,
        "genres": item.genres,
        "roles": []
    }
    for staff in kinopoisk.get_film_staff(item.kp_id):
        if not list(filter(lambda person: person['kp_id'] == staff.kp_id, persons)):
            person = kinopoisk.get_person(staff.kp_id)
            try:
                persons.append({
                    'kp_id': staff.kp_id,
                    'fullname': person.name,
                    'ru_fullname': person.ru_name,
                    'birth_date': person.birth_date,
                    'death': person.death,
                    'height': person.height,
                    'sex': person.sex
                })
            except AttributeError:
                continue
            else:
                save_json('persons.json', persons)
        movie['roles'].append({
            'role_name': staff.role_name,
            'role_type': staff.role,
            'person': staff.kp_id
        })
    top_movies.append(movie)
    save_json('movies.json', top_movies)
    end = time.time()
    print(end - start)
