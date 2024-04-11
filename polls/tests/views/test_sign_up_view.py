"""Unit tests of the Sign up view."""
from django.test import TestCase
from django.urls import reverse
from polls.forms import SignUpForm
from polls.models import User
from polls.tests.helpers import LogInTester

class SignUpViewTestCase(TestCase, LogInTester):

    fixtures = [
    'polls/tests/fixtures/users.json',
    'polls/tests/fixtures/unregistered_users.json',
    ]

    def setUp(self):
        self.url = reverse('sign_up')
        self.unregistered_user = User.objects.get(username = "JaneyID123")
        self.unregistered_user.set_unusable_password()
        self.unregistered_user.save()
        self.form_input = {
            'username': 'JaneyID123',
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }
        self.user = User.objects.get(username='JaneID123')

    def test_sign_up_url(self):
        self.assertEqual(self.url,'/polls/sign_up/')

    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertFalse(form.is_bound)

    def test_sign_up_redirects_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_unsuccessful_sign_up(self):
        self.form_input['username'] = 'INVALID_USERNAME'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_successful_sign_up(self):
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertTrue(self._is_logged_in())

    def test_sign_up_does_not_increase_number_of_users(self):
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_sign_up_with_existing_account_is_unsuccessful(self):
        self.form_input['username'] = 'JaneID123'
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_sign_up_without_existing_account(self):
        self.form_input['username'] = 'NonexistentID'
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())