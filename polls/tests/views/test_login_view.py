"""Unit tests of the Log in view."""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from polls.forms import LogInForm
from polls.models import User
from polls.tests.helpers import LogInTester, reverse_with_next

class LogInViewTestCase(TestCase, LogInTester):

    fixtures = [
    'polls/tests/fixtures/users.json',
    ]

    def setUp(self):
        self.url = reverse('log_in')
        self.user = User.objects.get(username='JaneID123')
        self.form_input = {
            'username': 'JaneID123',
            'password': 'Password123',
        }

    def test_log_in_url(self):
        self.assertEqual(self.url,'/polls/log_in/')

    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)

    def test_get_log_in_with_redirect(self):
        destination_url = reverse('dashboard')
        self.url = reverse_with_next('log_in', destination_url)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        next = response.context['next']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertEqual(next, destination_url)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_get_log_in_redirects_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_unsuccessful_log_in(self):
        self.form_input['password'] = 'WRONGPassword123'
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_successful_log_in(self):
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_log_in_with_blank_username(self):
        self.form_input['username'] = ''
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_log_in_with_blank_password(self):
        self.form_input['password'] = ''
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_post_log_in_redirects_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        self.form_input ['username'] = 'RandomName'
        self.form_input ['password'] = 'DoesntMatter'
        response = self.client.post(self.url, self.form_input, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')