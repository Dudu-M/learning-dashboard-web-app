"""Unit tests for the Dashboard view."""
from django.test import TestCase
from django.urls import reverse
from polls.models import User
from polls.tests.helpers import reverse_with_next

class DashboardViewTestCase(TestCase):
    fixtures = [
    'polls/tests/fixtures/users.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='JaneID123')
        self.url = reverse('dashboard')

    def test_dashboard_url(self):
        self.assertEqual(self.url,'/polls/dashboard/')

    def test_get_dashboard(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_get_dashboard_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)