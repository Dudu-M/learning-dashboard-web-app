"""Unit tests for the Overview view."""
from django.test import TestCase
from django.urls import reverse
from polls.models import User, Module, Resource
from polls.tests.helpers import reverse_with_next

class OverviewViewTestCase(TestCase):
    fixtures = [
        'polls/tests/fixtures/users.json',
        'polls/tests/fixtures/modules.json',
        'polls/tests/fixtures/resources.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='JaneID123')
        self.module = Module.objects.get(id = 1)
        self.user.modules.add(self.module)
        self.url = reverse('overview')
        
    def test_module_overview_url(self):
        self.assertEqual(self.url, '/polls/overview/')

    def test_get_overview(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'overview.html')
        
    def test_get_overview_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        
    def test_get_overview_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)