"""Unit tests for the log out view."""
from django.test import TestCase
from django.urls import reverse
from polls.models import User
from polls.tests.helpers import LogInTester

class LogOutViewTestCase(TestCase, LogInTester):

    fixtures = [
    'polls/tests/fixtures/users.json',
    ]

    def setUp(self):
        self.url = reverse('log_out')
        self.user = self.user = User.objects.get(username='JaneID123')

    def test_log_out_url(self):
        self.assertEqual(self.url,'/polls/log_out/')

    def test_successful_log_out(self):
        self.client.login(username='JaneID123', password = 'Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        response_url = reverse('log_in')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'log_in.html')
        self.assertFalse(self._is_logged_in())

    def test_cannot_log_out_without_being_logged_in(self):
        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        response_url = reverse('log_in')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'log_in.html')
        self.assertFalse(self._is_logged_in())