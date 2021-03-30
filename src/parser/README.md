# Movies and Persons seeds generator

## Start

1. Get api-key from https://kinopoiskapiunofficial.tech/ 
2. Set env variables 
```shell
set KP_API_KEY='YOUR_API_KEY'
```
3. Run parser.py
4. Run formatter.py
5. Run
```shell
cd ..
manage.py loaddata seed/movies.json
manage.py loaddata seed/persons.json
```