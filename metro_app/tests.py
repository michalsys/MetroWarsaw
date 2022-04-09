import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from metro_app.models import Character


@pytest.mark.django_db
def test_check_index():
    client = Client()
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_check_create_character(user):
    client = Client()
    url = reverse('new_game')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_character(user, location):
    url = reverse('new_game')
    client = Client()
    client.force_login(user)
    d = {
        'name': 'a'
    }
    response = client.post(url, d)
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_character_not_logged():
    client = Client()
    url = reverse('new_game')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_check_character_list(user, characters):
    client = Client()
    client.force_login(user)
    url = reverse('character_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == len(characters)
    for character in characters:
        assert character in response.context['object_list']


@pytest.mark.django_db
def test_character_list_not_logged():
    client = Client()
    url = reverse('character_list')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_check_rest_view(user, character_rest):
    client = Client()
    url = reverse('rest', args=[character_rest.id])
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_rest_view(user, character_rest):
    client = Client()
    url = reverse('rest', args=[character_rest.id])
    client.force_login(user)
    character_health = character_rest.health
    character_bullets = character_rest.bullets
    response = client.post(url)
    character_rest.refresh_from_db()
    assert response.status_code == 302
    assert character_rest.bullets == character_bullets - 5
    if character_health >= 5:
        assert character_rest.health == 10
    else:
        assert character_rest.health == character_health + 5


@pytest.mark.django_db
def test_rest_view_not_logged(character_fresh):
    client = Client()
    url = reverse('rest', args=[character_fresh.id])
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_rest_view_too_poor(user, character_fresh):
    client = Client()
    url = reverse('rest', args=[character_fresh.id])
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_check_victory_view(user, character_victory):
    client = Client()
    url = reverse('victory', args=[character_victory.id])
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_victory_view(user, character_victory):
    client = Client()
    url = reverse('victory', args=[character_victory.id])
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert character_victory not in Character.objects.all()


@pytest.mark.django_db
def test_victory_view_not_logged(character_victory):
    client = Client()
    url = reverse('victory', args=[character_victory.id])
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_victory_view_too_poor(user, character_fresh):
    client = Client()
    url = reverse('victory', args=[character_fresh.id])
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_check_death_view(user, character_death):
    client = Client()
    url = reverse('death', args=[character_death.id])
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_death_view(user, character_death):
    client = Client()
    url = reverse('death', args=[character_death.id])
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert character_death not in Character.objects.all()


@pytest.mark.django_db
def test_death_view_not_logged(character_death):
    client = Client()
    url = reverse('death', args=[character_death.id])
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_death_view_too_healthy(user, character_fresh):
    client = Client()
    url = reverse('death', args=[character_fresh.id])
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_game_view_death(user, character_death, locations, events, factions, enemies):
    client = Client()
    url = reverse('game', args=[character_death.id])
    client.force_login(user)
    response = client.post(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_game_view_victory(user, character_victory, locations, events, factions, enemies):
    client = Client()
    url = reverse('game', args=[character_victory.id])
    client.force_login(user)
    response = client.post(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_game_view(user, character_fresh, locations, events, factions, enemies):
    client = Client()
    url = reverse('game', args=[character_fresh.id])
    client.force_login(user)
    character_location = character_fresh.location
    response = client.post(url)
    character_fresh.refresh_from_db()
    assert response.status_code == 200
    assert character_location != character_fresh.location
