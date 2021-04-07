import asyncio
import os
from datetime import date
from os import getenv
from pprint import pprint

from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand

from movies.models import Poster, Movie, Genre
from person.models import Person, Photo, PersonRole
from parser.formatter import get_formatted_movie_fields, get_formatted_person_fields, get_formatted_role_fields
from parser.kinopoisk_api import KP
from argparse import ArgumentParser


class Command(BaseCommand):
    help = 'Get full film info from kinopoisk and add to database'

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('movie_id', type=int)
        parser.add_argument('-k', '--api-key', default=getenv('KP_API_KEY'))

    async def _get_movie_info(self, kp: KP, movie_id: int):
        movie, persons = await kp.get_full_film_info(movie_id)
        posters = await kp.get_film_photo(movie_id)
        kp.REQUESTS_LIMIT = 50
        photos_tasks = [asyncio.create_task(kp.get_person_photo(person["kp_id"])) for person in persons]
        photos = await asyncio.gather(*photos_tasks)
        return {
            'movie': movie,
            'posters': posters,
            'persons': persons,
            'photos': photos
        }

    def _get_kp_id_from_image_data(self, image_data: dict):
        filename: str = next(iter(image_data))
        return int(filename.removesuffix('.jpg').removeprefix('person_').removeprefix('movie_'))

    @staticmethod
    def safe_mkdir(dirname):
        if not os.path.exists(dirname):
            os.mkdir(dirname)

    def add_person(self, raw_person_data: dict, photos) -> tuple[int, Person]:
        kp_id = int(raw_person_data.pop('kp_id'))
        person_data = get_formatted_person_fields(raw_person_data)
        person_data['birth_date'] = date(*map(int, birth_date.split('-'))) \
            if (birth_date := person_data['birth_date']) else None
        person_data['death'] = date(*map(int, birth_date.split('-'))) \
            if (birth_date := person_data['death']) else None
        person: Person = Person.objects.get_or_create(**person_data)[0]
        if not person.photos.exists() and (image_bin := next(iter(photos[kp_id].values()))):
            self.safe_mkdir('temp')
            file_path = os.path.join('temp', next(iter(photos[kp_id])))
            with open(file_path, 'wb') as f:
                f.write(image_bin)
            try:
                Photo(image=ImageFile(open(file_path, 'rb')),
                      person=person,
                      orientation=Photo.OrientationType.VERTICAL.name,
                      format=Photo.FormatType.MEDIUM.name).save()
            finally:
                os.remove(file_path)
        return kp_id, person

    def handle(self, *args, **options):
        movie_id = options['movie_id']
        kinopoisk = KP(options['api_key'])
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self._get_movie_info(kinopoisk, movie_id))
        loop.run_until_complete(future)
        full_movie_info: dict = future.result()
        self.stdout.write("Data received")

        movie_info: dict = full_movie_info['movie']
        genres = [Genre.objects.get_or_create(title=genre)[0] for genre in movie_info['genres']]
        formatted_movie_info = get_formatted_movie_fields(movie_info)
        # movie = Movie.objects.filter(**formatted_movie_info).first()
        if Movie.objects.filter(**formatted_movie_info).exists():
            self.stdout.write(f"Movie {movie_id} exists in this database")
            return
        formatted_movie_info['movie_type_id'] = formatted_movie_info.pop('movie_type')
        movie: Movie = Movie(**formatted_movie_info)
        movie.save()
        for genre in genres:
            movie.genres.add(genre)
        self.stdout.write("Movie saved")
        photos = {self._get_kp_id_from_image_data(image_data): image_data for image_data in full_movie_info['photos']}

        persons_kp_id_map = {}
        raw_person_data: dict
        for raw_person_data in full_movie_info['persons']:
            kp_id, person = self.add_person(raw_person_data, photos)
            persons_kp_id_map[kp_id] = person

        self.stdout.write("Persons saved")

        for role in movie_info['roles']:
            PersonRole(**get_formatted_role_fields(role, movie, persons_kp_id_map[int(role['kp_id'])])).save()
        self.stdout.write("Roles saved")

        for filename, image_bin in full_movie_info['posters'].items():
            if not image_bin:
                continue
            self.safe_mkdir('temp')
            file_path = os.path.join('temp', filename)
            with open(file_path, 'wb') as f:
                f.write(image_bin)
            try:
                Poster(movie=movie,
                       image=ImageFile(open(file_path, 'rb')),
                       orientation=Poster.OrientationType.VERTICAL.name,
                       format=Poster.FormatType.LARGE.name if '_small' in filename else Poster.FormatType.LARGE.name). \
                    save()
            finally:
                os.remove(file_path)
        os.rmdir('temp')
        self.stdout.write("Posters saved")
