import asyncio
from os import getenv, mkdir
from kinopoisk_api import KP
import time
from utils import load_json


def _get_tasks(objects, worker, *args, **kwargs):
    return [asyncio.create_task(worker(object["kp_id"], *args, **kwargs)) for object in objects]


async def get_movies_posters(kp: KP, assets_folder: str):
    movies = load_json('parser/movies.json')
    print("Movies started")
    await asyncio.gather(*_get_tasks(movies, kp.get_film_photo, assets_folder=assets_folder))
    print("Movies Done!")


async def get_persons_photos(kp: KP, assets_folder: str):
    persons = load_json('parser/persons.json')
    print("Persons started")
    await asyncio.gather(*_get_tasks(persons, kp.get_person_photo, assets_folder=assets_folder))
    print("Persons Done")


async def main():
    try:
        mkdir('assets')
    except FileExistsError:
        pass
    program_start = time.time()
    kinopoisk = KP(token=getenv('KP_API_KEY'), requests_limit=50)
    await get_movies_posters(kinopoisk, 'assets')
    print(round((time.time() - program_start) / 60, 2))
    await get_persons_photos(kinopoisk, 'assets')
    print(round((time.time() - program_start) / 60, 2))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(main())
    loop.run_until_complete(future)
