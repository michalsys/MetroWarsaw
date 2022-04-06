import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_register_and_login_user():
    url = reverse('register')
    client = Client()
    d = {
        'username': 'a',
        'password_1': 'b',
        'password_2': 'b',
        'email': 'abc@o2.pl'
    }
    response = client.post(url, d)
    assert response.status_code == 302
    User.objects.get(username='a')
    assert client.login(username='a', password='b')
