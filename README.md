# Kinopoisk on Django

* [Description](#description)
    * [Short](#short)
    * [Full](#full)
* [Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
    * [Install & Run project](#install--run-project)
    * [Seed data](#seed-data)
        * [Base (Top 250 kinopoisk movies)](#base-top-250-kinopoisk-movies)
        * [Add movie from kinopoisk](#add-movie-from-kinopoisk)
        * [Generate movie score](#generate-movie-score)
* [Built With](#built-with)
* [Contributing](#contributing)
    * [Code Style](#code-style)
    * [Tasks](#tasks)
    * [Branch naming](#branch-naming)
* [Authors](#authors)
* [License](#license)
* [Environment variables](#environment-variables)

## Description

### Short
Aggregator of movies

### Full
A clone of kinopoisk. <br>
At the moment, the user can view information about movies and persons, <br>
watch news

## Getting Started

### Prerequisites

1. [Python3](https://www.python.org)
2. [PostgreSQL](https://www.postgresql.org)
3. [Minio](https://docs.min.io)

### Install & Run project

1. Clone repo 
```shell
git clone https://github.com/Pogchamp-company/kinopoisk_on_django.git
```
2. Create Python Virtual Environment
3. Install requirements
```shell
pip install -r requirements.txt
```
4. Create PostgreSQL database
5. Set [env variables](#environment-variables)
6. Migrate database
```shell
# cd src
manage.py migrate
```
7. Run minio
```shell
# cd ..
docker-compose up -d minio
```   
8. Initialize Minio buckets
```shell
manage.py initialize_buckets
```
9. Collect static files
```shell
manage.py collectstatic
```
10. Optional: [run seeds](#seed-data)
11. Run project
```shell
manage.py runserver
```


### Seed data
#### Base (Top 250 kinopoisk movies)
1. [Generate seeders json](https://github.com/Pogchamp-company/kinopoisk_on_django/tree/master/src/parser#generate-seeds) or download this in [release](https://github.com/Pogchamp-company/kinopoisk_on_django/releases/tag/v0.2-beta)
2. Run
```shell
manage.py loaddata seed/movies.json
manage.py loaddata seed/persons.json
``` 
3. [Get posters](https://github.com/Pogchamp-company/kinopoisk_on_django/tree/master/src/parser#collect-images)
4. Run
```shell
manage.py load_posters
manage.py load_photos
``` 
#### Add movie from kinopoisk
[YOUR_API_KEY](https://kinopoiskapiunofficial.tech/)

Run
```shell
manage.py add_kp_movie {movie_id} --api-key {YOUR_API_KEY}
```
#### Generate movie score
Run
```shell
manage.py seed_users {users_count}
manage.py seed_scores
```

## Run tests

<b>!Warning:</b> [seed data](#seed-data) before running tests

```shell
bash run_tests.sh
```


## Built With

* [Django](https://github.com/django/django) - The web framework used
* [Django Rest Framework](https://github.com/encode/django-rest-framework) - Rest api utils

## Contributing

### Code style
[pep8](https://www.python.org/dev/peps/pep-0008/)

### Tasks

* [Trello Desk](https://trello.com/b/fju3vs7M/kinopoisk-on-django)

### Branch naming

{username}/{task_short_description}


## Authors

* **Roman Alexandrov** - *Documentation, Backend* - [Github](https://github.com/AlexandrovRoman)
* **Artem Golovin** - *Backend* - [Github](https://github.com/RustyGuard)
* **Sergey Sirotkin** - *Main frontend developer* - [Github](https://github.com/najisirotkin)


## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/Pogchamp-company/kinopoisk_on_django/blob/master/LICENSE.md) file for details


## Environment variables

| Variable        | Short description | Default |
| ------------- |:-------------:| -----:|
| SECRET_KEY | App session secret key | @oowa+)%q57uxhffto99*-b+mt%63!@r&*#17mqstv&%fr9*2* |
| DATABASE_URI | PostgreSQL connection URI | postgresql+psycopg2://postgres@localhost:5432/KOD |
| MINIO_ENDPOINT | Endpoint to connect minio | 127.0.0.1:9001 |
| MINIO_ACCESS_KEY | Minio user | minio |
| MINIO_SECRET_KEY | Minio password | minio123 |
| MINIO_USE_HTTPS | - | False |
