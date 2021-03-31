from utils import load_json, save_json

try:
    movie_list_json = load_json('movies.json')
    person_list_json = load_json('persons.json')
except FileNotFoundError:
    print('Run src/parser.parser.py to get raw json data')
    raise

movies_model_list = [
    {
        'model': 'movies.movietype',
        'pk': 1,
        'fields': {
            'title': 'Сериал'
        }
    },
    {
        'model': 'movies.movietype',
        'pk': 2,
        'fields': {
            'title': 'Фильм'
        }
    },
]
person_model_list = []

persons_kp_id_map = {}
for i, person in enumerate(person_list_json, 1):
    persons_kp_id_map[person['kp_id']] = i
    if len(person['sex']) > 6:
        person['sex'] = 'MALE'
    person_model_list.append({
        'model': 'person.person',
        'pk': i,
        'fields': {
            'fullname': person['fullname'] or person['ru_fullname'],
            'ru_fullname': person['ru_fullname'],
            'birth_date': person['birth_date'],
            'death': person['death'],
            'height': person['height'] if person['height'] else None,
            'sex': person['sex'],
        }
    })

genres = {}
last_genre_id = 1
last_role_id = 1
reformat_casing = lambda string: string.replace('-', '_') if string else None
for i, movie_json in enumerate(movie_list_json, 1):
    movie_genres = []
    for genre in movie_json['genres']:
        if genre_id := genres.get(genre, None):
            movie_genres.append(genre_id)
        else:
            genres[genre] = last_genre_id
            movie_genres.append(last_genre_id)
            movies_model_list.append({
                'model': 'movies.genre',
                'pk': last_genre_id,
                'fields': {
                    'title': genre
                }
            })
            last_genre_id += 1
    for role in movie_json['roles']:
        if role['role'] == 'PRODUCER_USSR':
            role['role'] = 'PRODUCER'
            if role['role_name']:
                role['role_name'] = f'{role["role_name"]} директор картины'
            else:
                role['role_name'] = 'директор картины'
        person_model_list.append({
            'model': 'person.personrole',
            'pk': last_role_id,
            'fields': {
                'role_name': role['role_name'],
                'role_type': role['role'],
                'person': persons_kp_id_map[role['kp_id']],
                'movie': i
            }
        })
        last_role_id += 1
    movies_model_list.append({
        'model': 'movies.movie',
        'pk': i,
        'fields': {
            'movie_type': 2 if movie_json['movie_type'] == 'FILM' else 1,
            'title': movie_json['title'],
            'original_title': movie_json['original_title'] if movie_json['original_title'] else movie_json['title'],
            'duration': movie_json['duration'],
            'slogan': movie_json['slogan'],
            'description': movie_json['description'],
            'premiere': movie_json['premiere'],
            'premiere_ru': movie_json['premiere_ru'],
            'rating_mpaa': reformat_casing(movie_json['rating_mpaa']),
            'age_rating': movie_json['age_rating'],
            'year': int(movie_json['year']),
            'budget': 5_000_000,
            'genres': movie_genres
        }
    })

save_json('../seed/movies.json', movies_model_list)
save_json('../seed/persons.json', person_model_list)
