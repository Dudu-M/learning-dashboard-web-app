"""Unit tests of the log in form."""
from django import forms
from django.test import TestCase
from polls.forms import LogInForm
from polls.models import User

class LogInFormTestCase(TestCase):

    fixtures = ['polls/tests/fixtures/users.json']

    def setUp(self):
        self.form_input = {'username': 'JaneID123', 'password': 'Password123'}

    def test_form_contains_required_fields(self):
        form = LogInForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
        password_field = form.fields['password']
        username_field = form.fields['username']
        self.assertTrue(isinstance(password_field.widget,forms.PasswordInput))
        self.assertTrue(isinstance(username_field, forms.CharField))
        
    def test_form_accepts_valid_input(self):
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        
    def test_form_does_not_accept_blank_username(self):
        self.form_input['username'] = ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        
    def test_form_accepts_incorrect_username(self):
        self.form_input['username'] = 'WrongUsername'
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_does_not_accept_blank_password(self):
        self.form_input['password'] = ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        
    def test_form_accepts_incorrect_password(self):
        self.form_input['password'] = 'WrongPassword'
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        
    def test_can_authenticate_valid_user(self):
        fixture = User.objects.get(id=1)
        form_input = {'username': 'JaneID123', 'password': 'Password123'}
        form = LogInForm(data=form_input)
        user = form.get_user()
        self.assertEqual(user, fixture)
        
    def test_invalid_credentials_do_not_authenticate(self):
        form_input = {'username': 'InvalidID', 'password': 'WrongPassword123'}
        form = LogInForm(data=form_input)
        user = form.get_user()
        self.assertEqual(user, None)

    def test_blank_password_does_not_authenticate(self):
        form_input = {'username': 'JaneID123', 'password': ''}
        form = LogInForm(data=form_input)
        user = form.get_user()
        self.assertEqual(user, None)

    def test_blank_username_does_not_authenticate(self):
        form_input = {'username': '', 'password': 'Password123'}
        form = LogInForm(data=form_input)
        user = form.get_user()
        self.assertEqual(user, None)