import pytest
from random import randint
from django.contrib.auth.models import User

from metro_app.models import Character, Location, Event, Faction, Enemy


@pytest.fixture
def user():
    user = User.objects.create(username='x')
    return user


@pytest.fixture
def location():
    location = Location.objects.create(name='x', threat_level='1')
    return location


@pytest.fixture
def event():
    event = Event.objects.create(name='y')
    return event


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


@pytest.fixture
def locations():
    locations = []
    for x in range(10):
        location = Location.objects.create(
            name='x', threat_level='1'
        )
        locations.append(location)
    return locations


@pytest.fixture
def events():
    events = []
    for x in range(10):
        event = Event.objects.create(
            name='x'
        )
        events.append(event)
    return events


@pytest.fixture
def factions():
    factions = []
    for x in range(10):
        faction = Faction.objects.create(
            name='x'
        )
        factions.append(faction)
    return factions


@pytest.fixture
def enemies():
    enemies = []
    for x in range(10):
        enemy = Enemy.objects.create(
            name='x'
        )
        enemies.append(enemy)
    return enemies
