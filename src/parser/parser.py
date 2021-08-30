import asyncio
from os import getenv
from kinopoisk_api import KP, SEARCH
import time
from utils import save_json


async def main():
    program_start = time.time()
    kinopoisk = KP(token=getenv('KP_API_KEY'))
    top250 = kinopoisk.top250()
    movies = []
    persons = []
    item: SEARCH
    for i, item in enumerate(top250, start=1):
        start = time.time()
        print(i, item.name)
        movie_info, movie_persons = await kinopoisk.get_full_film_info(item.kp_id)
        movies.append(movie_info)
        persons.extend(movie_persons)
        end = time.time()
        print(end - start)
        save_json('movies.json', movies)
        save_json('persons.json', list(persons))
    print(round((time.time() - program_start) / 60, 2))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(main())
    loop.run_until_complete(future)
