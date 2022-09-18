import asyncio
import os
import time
import xml.etree.ElementTree as xml
from pprint import pprint

from aiohttp import ClientSession, ClientTimeout
from aiohttp.web_exceptions import HTTPTooManyRequests
from json import JSONDecodeError

import requests
import json


class FILM:
    def __init__(self, data: dict):
        self.kp_id = data['filmId']
        self.name = data['nameRu'] if data['nameEn'] == '' else data['nameEn']
        self.ru_name = data['nameRu']
        self.type = data['type']
        self.year = data['year'].split('-')[0] if not isinstance(data['year'], int) else data['year']
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
        self.roles = []

    def to_dict(self):
        return {
            "kp_id": self.kp_id,
            "title": self.ru_name,
            "original_title": self.name,
            "movie_type": self.type,
            "year": self.year,
            "slogan": self.tagline,
            "description": self.description,
            "duration": self.duration + ":00" if self.duration else None,
            "premiere": self.premiere,
            "premiere_ru": self.premiere_ru,
            "rating_mpaa": self.mpaa_rating,
            "age_rating": self.age_rating,
            "kp_rate": self.kp_rate,
            "imdb_rate": self.imdb_rate,
            "genres": self.genres,
            "roles": self.roles,
        }


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
    def __init__(self, token, secret=None, requests_limit=15):
        self.token = token
        self.secret = secret
        self.headers = {"X-API-KEY": self.token}
        self.api_versions = {
            'staff': 'v1',
            'movie': 'v2.1',
            'top': 'v2.2'
        }
        self.base_api_url = 'https://kinopoiskapiunofficial.tech/api/'
        self.api_endpoints = {
            'staff': f'{self.base_api_url}{self.api_versions["staff"]}/staff',
            'movie': f'{self.base_api_url}{self.api_versions["movie"]}/films/' + '{film_id}',
            'search': f'{self.base_api_url}{self.api_versions["movie"]}/films/search-by-keyword',
            'top': f'{self.base_api_url}{self.api_versions["top"]}/films/top?type=' + '{type}',
            'image': 'https://kinopoiskapiunofficial.tech/images/{container}/kp{size}/{kp_id}.jpg'
        }
        self.about = 'KinoPoiskAPI'
        self.requests_count = 0
        self.REQUESTS_LIMIT = requests_limit

    async def get_film(self, film_id: int, session: ClientSession):
        rate_request = await self.request(f'https://rating.kinopoisk.ru/{film_id}.xml', session)
        try:
            kp_rate = xml.fromstring(rate_request)[0].text
        except (IndexError, TypeError):
            kp_rate = 0
        try:
            imdb_rate = xml.fromstring(rate_request)[1].text
        except (IndexError, TypeError):
            imdb_rate = 0

        request_json = await self.request(self.api_endpoints['movie'].format(film_id=film_id), session)
        request_json['data']['kp_rate'] = float(kp_rate)
        request_json['data']['imdb_rate'] = float(imdb_rate)
        return FILM(request_json['data'])

    def search(self, query):
        output = []
        for _ in range(10):
            try:
                request = requests.get(self.api_endpoints['search'], headers=self.headers,
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
                request = requests.get(self.api_endpoints['top'].format(type='TOP_250_BEST_FILMS') + f'&page={page}',
                                       headers=self.headers
                                       )
                request_json = json.loads(request.text)
                for film in request_json['films']:
                    output.append(SEARCH(film))
            except json.decoder.JSONDecodeError:
                time.sleep(0.5)
                continue
        return output

    def get_film_staff(self, film_id: int):
        request = requests.get(f'{self.api_endpoints["staff"]}?filmId={film_id}', headers=self.headers)
        try:
            data = json.loads(request.text)
        except JSONDecodeError:
            time.sleep(1)
            return self.get_film_staff(film_id)
        for staff in data:
            yield STAFF(staff)

    def get_person(self, person_id: int):
        request = requests.get(f'{self.api_endpoints["staff"]}/{person_id}', headers=self.headers)
        try:
            data = json.loads(request.text)
        except JSONDecodeError:
            if request.status_code == 404:
                return
            time.sleep(1)
            return self.get_person(person_id)
        return PERSON(data)

    async def _get_image(self, container_name: str, kp_id: int, size=""):
        async with ClientSession(timeout=ClientTimeout(total=500), headers=self.headers) as session:
            content = await self.request(self.api_endpoints["image"].format(container=container_name, size=size, kp_id=kp_id), session, 'image/jpeg')
            return content

    def _save_image(self, filename, data, assets_folder=""):
        with open(os.path.join(assets_folder, filename), "wb") as f:
            f.write(data)

    async def get_person_photo(self, person_id: int, assets_folder=None):
        filename = f"person_{person_id}.jpg"
        if assets_folder is not None and os.path.exists(os.path.join(assets_folder, filename)):
            print(f"{filename} exists")
            return
        photo = await self._get_image('actor_posters', person_id)
        if assets_folder is not None and photo:
            print(f'{filename} collected')
            self._save_image(filename, photo, assets_folder)
        if assets_folder is None:
            return {filename: photo}

    async def get_film_photo(self, film_id: int, assets_folder=None):
        large_poster_filename = f"movie_{film_id}.jpg"
        small_poster_filename = f"movie_{film_id}_small.jpg"
        large = await self._get_image('posters', film_id)
        small = await self._get_image('posters', film_id, "_small")
        resp = {large_poster_filename: large, small_poster_filename: small}
        if assets_folder is not None and large and small:
            self._save_image(large_poster_filename, large, assets_folder)
            self._save_image(small_poster_filename, small, assets_folder)
        if assets_folder is None:
            return resp

    async def request(self, url, session, allowed_content_type=None):
        while self.requests_count > self.REQUESTS_LIMIT:
            await asyncio.sleep(.25)
        self.requests_count += 1
        async with session.get(url) as response:
            self.requests_count -= 1
            if response.status == 200:
                if allowed_content_type and response.content_type != allowed_content_type:
                    return
                if response.content_type == 'application/json':
                    return await response.json()
                elif response.content_type == 'text/html':
                    return await response.text()
                else:
                    return await response.content.read()
            elif response.status == 404:
                return {}
            elif response.status == 429:
                print("Limit exceeded")
                print(f"Old limit: {self.REQUESTS_LIMIT}")
                if self.REQUESTS_LIMIT > 3:
                    self.REQUESTS_LIMIT -= 1
                else:
                    raise HTTPTooManyRequests
                print(f"New limit: {self.REQUESTS_LIMIT}")
                return await self.request(url, session)

    async def get_full_film_info(self, film_id):
        person_tasks = []
        async with ClientSession(timeout=ClientTimeout(total=500), headers=self.headers) as session:
            movie = await self.get_film(film_id, session)
            roles = await self.request(f'{self.api_endpoints["staff"]}?filmId={film_id}', session)
            for role in roles:
                staff = STAFF(role)
                movie.roles.append(staff.__dict__)
                task_request = asyncio.create_task(self.request(f'{self.api_endpoints["staff"]}/{staff.kp_id}', session))
                person_tasks.append(task_request)
            raw_persons = await asyncio.gather(*person_tasks)
            persons = []
            for person in raw_persons:
                try:
                    persons.append(PERSON(person).to_dict())
                except KeyError:
                    pass
            return movie.to_dict(), persons


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
        self.fullname = data['nameRu'] if data['nameEn'] == '' else data['nameEn']
        self.ru_fullname = data['nameRu']
        self.sex = data['sex']
        self.height = data['growth']
        self.birth_date = data['birthday']
        self.death = data['death']

    def to_dict(self):
        return self.__dict__
