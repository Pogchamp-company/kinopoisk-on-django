import os

from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand

from movies.models import Poster, Movie
from parser.utils import load_json
from utils.mixins import Image


class Command(BaseCommand):
    help = 'Loads posters for top 250 films from assets folder'

    def handle(self, *args, **options):
        movies = load_json('parser/movies.json')
        movies_map = {movie['kp_id']: movie for movie in movies}

        for file in os.listdir('parser/assets'):
            full_file_path = os.path.join('parser', 'assets', file)
            if file.startswith('movie_'):
                self.stdout.write(self.style.SUCCESS(file))
                kp_id = int(file.removeprefix('movie_').removesuffix('.jpg').removesuffix('_small'))
                movie = movies_map.get(kp_id, None)
                if not movie:
                    self.stdout.write(f'Movie with {kp_id=} not found')
                    continue
                poster = Poster()
                poster.image = ImageFile(open(full_file_path, "rb"))

                poster.movie = Movie.objects.filter(title=movie['title']).first()
                poster.orientation = Image.OrientationType.VERTICAL.name
                poster.format = Image.FormatType.MEDIUM.name if '_small' in file else Image.FormatType.LARGE.name
                poster.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully loaded poster {poster.movie}'))
