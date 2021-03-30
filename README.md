# Kinopoisk on Django

## Description

### Short
Aggregator of movies

### Full
A clone of kinopoisk. <br>
At the moment, the user can view information about movies and persons, <br>
watch news

## Getting Started

### Prerequisites

1. Python3 [Docs](https://www.python.org)
2. PostgreSQL [Docs](https://www.postgresql.org)
3. Minio [Docs](https://docs.min.io)

### Installing

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
5. Set env variables ([Vars](#environment-variables))
6. Migrate database
```shell
cd src
manage.py migrate
```
7. Run minio
```shell
docker-compose up -d minio
```   
8. Initialize Minio buckets
```shell
manage.py initialize_buckets
```
9. Optional: run seeds (generate this (check src/parser/README.md) or download from release)
```shell
manage.py loaddata seed/movies.json
manage.py loaddata seed/persons.json
```   
10. Run project
```shell
manage.py runserver
```


## Built With

* [Django](https://github.com/django/django) - The web framework used
* [Django Rest Framework](https://github.com/encode/django-rest-framework) - Rest api utils

## Contributing

* [Trello Desk](https://trello.com/b/fju3vs7M/kinopoisk-on-django)

### Branch naming

{username}/{task_short_description}


## Authors

* **Alexandrov Roman** - *Documentation, Backend* - [Github](https://github.com/AlexandrovRoman)
* **Artem Golovin** - *Backend* - [Github](https://github.com/RustyGuard)
* **Sergey Sirotkin** - *Main frontend developer* - [Github](https://github.com/najisirotkin)


## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/Pogchamp-company/kinopoisk_on_django/blob/main/LICENSE.md) file for details


## Environment variables

| Variable        | Short description | Default |
| ------------- |:-------------:| -----:|
| POSTGRESQL_USER | PostgreSQL user | postgres |
| POSTGRESQL_PASSWORD | PostgreSQL user password | None |
| POSTGRESQL_HOST | PostgreSQL host | localhost |
| POSTGRESQL_PORT | PostgreSQL port | 5432 |
| DATABASE_NAME | PostgreSQL database | KOD |