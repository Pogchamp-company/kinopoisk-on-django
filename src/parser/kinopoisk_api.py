import asyncio
import os
import time
import xml.etree.ElementTree as xml
from aiohttp import ClientSession, ClientTimeout
from json import JSONDecodeError
from pprint import pprint

import requests
import json


class FILM:
    def __init__(self, data: dict):
        self.kp_id = data['filmId']
        self.name = data['nameRu'] if data['nameEn'] == '' else data['nameEn']
        self.ru_name = data['nameRu']
        self.type = data['type']
        self.year = data['year'].split('-')[0] if data['type'] != 'FILM' else data['year']
        self.duration = data['filmLength']
        self.tagline = data['slogan'] if data['slogan'] is not None else '-'
        self.description = data['description']
        self.genres = [genre['genre'] for genre in data['genres']]
        self.countries = [country['country'] for country in data['countries']]
        self.age_rating = data['ratingAgeLimits']
        self.mpaa_rating = data['ratingMpaa']
        self.kp_rate = data.get('kp_rate', None)
        self.imdb_rate = data.get('imdb_rate', None)
        self.kp_url = data['webUrl']
        self.premiere = data['premiereWorld']
        self.premiere_ru = data['premiereRu']
        self.poster = data['posterUrl']
        self.poster_preview = data['posterUrlPreview']


class SEARCH:
    def __init__(self, data: dict):
        self.kp_id = data['filmId']
        self.name = data['nameRu'] if not data['nameEn'] else data['nameEn']
        self.ru_name = data['nameRu']
        self.year = data['year'].split('-')[0]
        self.duration = data['filmLength']
        self.genres = [genre['genre'] for genre in data['genres']]
        self.countries = [country['country'] for country in data['countries']]
        self.kp_rate = data['rating']
        self.kp_url = f'https://www.kinopoisk.ru/film/{data["filmId"]}/'
        self.poster = data['posterUrl']
        self.poster_preview = data['posterUrlPreview']


class KP:
    def __init__(self, token, secret=None):
        self.token = token
        self.secret = secret
        self.headers = {"X-API-KEY": self.token}
        self.api_version = 'v2.1'
        self.staff_api_version = 'v1'
        self.API = 'https://kinopoiskapiunofficial.tech/api/' + self.api_version + '/'
        self.STAFF_API = f'https://kinopoiskapiunofficial.tech/api/{self.staff_api_version}/staff'
        self.secret_API = 'https://videocdn.tv/api/short'
        self.version = self.api_version + '.2-release'
        self.about = 'KinoPoiskAPI'
        self.requests_count = 0
        self.REQUESTS_LIMIT = 15

    def get_film(self, film_id):
        cache = CACHE().load()

        rate_request = requests.get(f'https://rating.kinopoisk.ru/{film_id}.xml').text
        try:
            kp_rate = xml.fromstring(rate_request)[0].text
        except IndexError:
            kp_rate = 0
        try:
            imdb_rate = xml.fromstring(rate_request)[1].text
        except IndexError:
            imdb_rate = 0

        if str(film_id) in cache:
            data = {}
            for a in cache[str(film_id)]:
                data[a] = cache[str(film_id)][a]
            data['kp_rate'] = kp_rate
            data['imdb_rate'] = imdb_rate
            return FILM(data)

        for _ in range(10):
            try:
                request = requests.get(self.API + 'films/' + str(film_id), headers=self.headers)
                request_json = json.loads(request.text)
                request_json['data']['kp_rate'] = kp_rate
                request_json['data']['imdb_rate'] = imdb_rate
                try:
                    if self.secret is not None:
                        request_secret = requests.get(self.secret_API, params={
                            "kinopoisk_id": film_id,
                            "api_token": self.secret
                        })
                        print(1, request_secret.text)
                        request_secret_json = json.loads(request_secret.text)
                        request_json['data']['secret'] = request_secret_json
                    else:
                        request_json['data']['secret'] = {"result": False}
                except (Exception, BaseException):
                    request_json['data']['secret'] = {"result": False}
                cache[str(film_id)] = request_json['data']
                CACHE().write(cache)
                return FILM(request_json['data'])
            except json.decoder.JSONDecodeError:
                time.sleep(0.5)
                continue

    def search(self, query):
        output = []
        for _ in range(10):
            try:
                request = requests.get(self.API + 'films/search-by-keyword', headers=self.headers,
                                       params={"keyword": query, "page": 1})
                request_json = json.loads(request.text)
                for film in request_json['films']:
                    try:
                        output.append(SEARCH(film))
                    except (Exception, BaseException):
                        continue
            except json.decoder.JSONDecodeError:
                time.sleep(0.5)
                continue
        return output

    def top250(self):
        output = []
        for page in range(1, 14):
            try:
                request = requests.get(f'{self.API}films/top?type=BEST_FILMS_LIST&page={page}&listId=1',
                                       headers=self.headers
                                       )
                request_json = json.loads(request.text)
                for film in request_json['films']:
                    output.append(SEARCH(film))
            except json.decoder.JSONDecodeError:
                time.sleep(0.5)
                continue
        return output

    async def top250_async(self):
        async with ClientSession(timeout=ClientTimeout(total=500), headers=self.headers) as session:
            tasks = []
            for page in range(1, 14):
                tasks.append(asyncio.create_task(
                    self.request(f'{self.API}films/top?type=BEST_FILMS_LIST&page={page}&listId=1', session)))
            result = await asyncio.gather(*tasks)
        output = []
        for page in result:
            for movie in page['films']:
                output.append(SEARCH(movie))
        return output

    def get_film_staff(self, film_id: int):
        request = requests.get(f'{self.STAFF_API}?filmId={film_id}', headers=self.headers)
        try:
            data = json.loads(request.text)
        except JSONDecodeError:
            time.sleep(1)
            return self.get_film_staff(film_id)
        for staff in data:
            yield STAFF(staff)

    def get_person(self, person_id: int):
        request = requests.get(f'{self.STAFF_API}/{person_id}', headers=self.headers)
        try:
            data = json.loads(request.text)
        except JSONDecodeError:
            if request.status_code == 404:
                return
            time.sleep(1)
            return self.get_person(person_id)
        return PERSON(data)

    async def request(self, url, session):
        while self.requests_count > self.REQUESTS_LIMIT:
            await asyncio.sleep(.25)
        self.requests_count += 1
        async with session.get(url) as response:
            self.requests_count -= 1
            html = await response.text()
            try:
                return json.loads(html)
            except JSONDecodeError:
                if response.status == 200:
                    return html
                elif response.status == 404:
                    return {}
                pprint(html)
                raise

    async def get_full_film_info(self, film_id):
        person_tasks = []
        async with ClientSession(timeout=ClientTimeout(total=500), headers=self.headers) as session:
            base_film_info = await self.request(f'{self.API}films/{film_id}', session)
            movie = FILM(base_film_info['data'])
            roles = await self.request(f'{self.STAFF_API}?filmId={film_id}', session)
            movie.roles = roles
            for role in roles:
                staff = STAFF(role)
                task_request = asyncio.create_task(self.request(f'{self.STAFF_API}/{staff.kp_id}', session))
                person_tasks.append(task_request)
            raw_persons = await asyncio.gather(*person_tasks)
            persons = []
            for person in raw_persons:
                try:
                    persons.append(PERSON(person).__dict__)
                except KeyError:
                    pass
            return movie.__dict__, persons


class CACHE:
    def __init__(self):
        self.PATH = os.path.dirname(os.path.abspath(__file__))

    def load(self) -> dict:
        try:
            with open(self.PATH + '/cache.json', 'r') as f:
                return json.loads(f.read())
        except FileNotFoundError:
            with open(self.PATH + '/cache.json', 'w') as f:
                f.write('{}')
                return {}

    def write(self, cache: dict, indent: int = 4):
        with open(self.PATH + '/cache.json', 'w') as f:
            return json.dump(cache, f, indent=indent)


class STAFF:
    def __init__(self, data: dict):
        self.kp_id = data["staffId"]
        self.name = data['nameRu'] if data['nameEn'] == '' else data['nameEn']
        self.ru_name = data['nameRu']
        self.role_name = data['description']
        self.role = data['professionKey']


class PERSON:
    def __init__(self, data: dict):
        self.kp_id = data["personId"]
        self.name = data['nameRu'] if data['nameEn'] == '' else data['nameEn']
        self.ru_name = data['nameRu']
        self.sex = data['sex']
        self.height = data['growth']
        self.birth_date = data['birthday']
        self.death = data['death']
