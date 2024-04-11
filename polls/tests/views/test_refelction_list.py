"""Unit tests for the Reflections List view."""
from django.test import TestCase
from django.urls import reverse
from polls.models import User, Plan, Reflection
from polls.tests.helpers import reverse_with_next

class PlansListViewTestCase(TestCase):
    fixtures = [
        'polls/tests/fixtures/users.json',
        'polls/tests/fixtures/plans.json',
        'polls/tests/fixtures/reflections.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='JaneID123')
        self.url = reverse('reflection_list')
        
    def test_reflections_list_url(self):
        self.assertEqual(self.url, '/polls/reflections/')

    def test_get_reflections_list(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reflections_list.html')
        
    def test_get_reflections_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        
    def test_get_reflections_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)