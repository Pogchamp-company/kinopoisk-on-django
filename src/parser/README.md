# Movies and Persons seeds generator

## Setup
1. Get [api-key](https://kinopoiskapiunofficial.tech/) 
2. Set env variables 
```shell
set KP_API_KEY='{YOUR_API_KEY}'
```

## Seed movies and persons
### Generate seeds
1. Run parser.py
2. Run formatter.py
### Seed to database   
Run
```shell
manage.py loaddata seed/movies.json
manage.py loaddata seed/persons.json
```

## Seed posters and photos
### Collect images
Run images_parser.py
### Seed images
Run 
```shell
manage.py load_posters
manage.py load_photos
```
