import os

from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand

from parser.utils import load_json
from utils.mixins import Image
from person.models import Photo, Person


class Command(BaseCommand):
    help = 'Loads photos for persons from top 250 films from assets folder'

    def handle(self, *args, **options):
        persons = load_json('parser/persons.json')
        for file in os.listdir('parser/assets'):
            full_file_path = os.path.join('parser', 'assets', file)
            if file.startswith('person_'):
                kp_id = int(file.removeprefix('person_').removesuffix('.jpg'))
                print(kp_id)
                for person in persons:
                    if person['kp_id'] == kp_id:
                        photo = Photo()
                        photo.image = ImageFile(open(full_file_path, "rb"))

                        photo.person = Person.objects.filter(fullname=person['fullname']).first()
                        print(photo.person)
                        photo.orientation = Image.OrientationType.VERTICAL.name
                        photo.format = Image.FormatType.LARGE.name
                        photo.save()
                        self.stdout.write(self.style.SUCCESS(f'Successfully loaded photo {photo.person}'))
                        break
                else:
                    print(f'Person with {kp_id=} not found')
