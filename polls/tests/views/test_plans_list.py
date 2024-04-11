"""Unit tests for the Plans List view."""
from django.test import TestCase
from django.urls import reverse
from polls.models import User, Plan
from polls.tests.helpers import reverse_with_next

class PlansListViewTestCase(TestCase):
    fixtures = [
        'polls/tests/fixtures/users.json',
        'polls/tests/fixtures/plans.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='JaneID123')
        self.plan = Plan.objects.get(id = 1)
        self.user.add_plan(self.plan)
        self.url = reverse('plans_list')
        
    def test_plans_list_url(self):
        self.assertEqual(self.url, '/polls/plans/')

    def test_get_plan_list(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plans_list.html')
        
    def test_get_plans_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        
    def test_get_plans_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)