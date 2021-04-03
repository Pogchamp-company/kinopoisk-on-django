# Movies and Persons seeds generator

## Start

### Setup
1. Get api-key from https://kinopoiskapiunofficial.tech/ 
2. Set env variables 
```shell
set KP_API_KEY='YOUR_API_KEY'
```

### Seed movies and persons
1. Run parser.py
2. Run formatter.py
3. Run
```shell
cd ..
manage.py loaddata seed/movies.json
manage.py loaddata seed/persons.json
```

### Seed posters and photos
1. Run images_parser.py
