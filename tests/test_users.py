import pytest
from django.urls import reverse
from django.contrib.auth import get_user

from apps.users.forms import CreateUserForm, ArchitectLoginForm


def test_create_user_form_fails_without_email():
    form = CreateUserForm(data={'username': 'Adam', 'email': ''})
    assert not form.is_valid()
    assert 'email' in form.errors


def test_create_user_form_password_label_is_correct():
    form = CreateUserForm()
    assert form.fields['password1'].label == 'Password'


def test_create_user_from_fails_if_username_taken(user):
    data = {
        'username': 'Adam',
        'email': 'test2@gmail.com',
        'password1': 'Haslo123!',
        'password2': 'Haslo123!',
    }

    form = CreateUserForm(data=data)
    assert not form.is_valid()
    assert 'username' in form.errors


def test_login_form_has_correct_username_placeholder():
    form = ArchitectLoginForm()
    assert form.fields['username'].widget.attrs['placeholder'] == 'neo_architect'


def test_login_form_has_correct_username_label():
    form = ArchitectLoginForm()
    assert form.fields['username'].label == "Identifier_Username"


@pytest.mark.django_db
def test_registration_flow_logs_in_user_automatically(client):
    url = reverse('register')
    data = {
        'username': 'Nowy',
        'email': 'nowy@gmail.com',
        'password1': 'Haslo123!',
        'password2': 'Haslo123!',
    }
    client.post(url, data)

    current_user = get_user(client)
    assert get_user(client).is_authenticated
    assert current_user.username == 'Nowy'
