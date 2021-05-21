from rest_framework import serializers
from person.models import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'ru_fullname', 'fullname')
