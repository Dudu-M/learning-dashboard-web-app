"""Unit tests of the Sign up form."""
from django.contrib.auth.hashers import check_password
from django import forms
from django.test import TestCase
from polls.forms import SignUpForm
from polls.models import User

class SignUpFormTestCase(TestCase):

    fixtures = [
    'polls/tests/fixtures/unregistered_users.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='JaneyID123')
        self.user.set_unusable_password()
        self.user.save()

        self.form_input = {
            'username': 'JaneyID123',
            'new_password': 'Password123!',
            'password_confirmation': 'Password123!'
        }

    def test_valid_sign_up_form(self):
        form = SignUpForm(data = self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = SignUpForm()
        self.assertIn('username', form.fields)
        self.assertIn('new_password', form.fields)
        new_password_widget = form.fields['new_password'].widget
        self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))
        self.assertIn('password_confirmation', form.fields)
        password_confirmation_widget = form.fields['password_confirmation'].widget
        self.assertTrue(isinstance(password_confirmation_widget, forms.PasswordInput))

    def test_password_must_contain_uppercase_character(self):
        self.form_input['new_password'] = 'password123'
        self.form_input['password_confirmation'] = 'password123'
        form = SignUpForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase_character(self):
        self.form_input['new_password'] = 'PASSWORD123'
        self.form_input['password_confirmation'] = 'PASSWORD123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input['new_password'] = 'PasswordABC'
        self.form_input['password_confirmation'] = 'PasswordABC'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_and_password_confirmation_are_identical(self):
        self.form_input['password_confirmation'] = 'WrongPassword123'
        form = SignUpForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_verifies_studentID_exists(self):
        fixture = User.objects.get(username='JaneyID123')
        form = SignUpForm(data = self.form_input)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.save(), fixture)

    def test_non_existent_studentID_cannot_does_not_allow_sign_up(self):
        self.form_input['username'] = 'NonExistentID'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
