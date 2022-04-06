import pytest
from random import randint
from django.contrib.auth.models import User

from metro_app.models import Character, Location


@pytest.fixture
def user():
    user = User.objects.create(username='x')
    return user


@pytest.fixture
def location():
    location = Location.objects.create(name='x', threat_level='1')
    return location


@pytest.fixture
def character_fresh(user, location):
    character = Character.objects.create(name='x', user=user, location=location)
    return character


@pytest.fixture
def character_rest(user, location):
    character = Character.objects.create(name='x', user=user, location=location,
                                         health=randint(1, 10), bullets=randint(5, 99))
    return character


@pytest.fixture
def character_victory(user, location):
    character = Character.objects.create(name='x', user=user, location=location, bullets=randint(100, 199))
    return character


@pytest.fixture
def character_death(user, location):
    character = Character.objects.create(name='x', user=user, location=location, health=randint(-10, 0))
    return character


@pytest.fixture
def characters(user, location):
    characters = []
    for x in range(5):
        character = Character.objects.create(
            name='x', user=user, location=location
        )
        characters.append(character)
    return characters
