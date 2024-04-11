"""Unit tests for the Show Plan view."""
from django.test import TestCase
from django.urls import reverse
from polls.models import User, Plan
from polls.tests.helpers import reverse_with_next

class ShowPlanViewTestCase(TestCase):
    fixtures = [
        'polls/tests/fixtures/users.json',
        'polls/tests/fixtures/plans.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='JaneID123')
        self.plan = Plan.objects.get(id = 1)
        self.url = reverse('show_plan', kwargs={'plan_id': self.plan.id})
        
    def test_show_plan_url(self):
        self.assertEqual(self.url, f'/polls/plan/{self.plan.id}')

    def test_get_show_plan(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_plan.html')
        
    def test_get_show_plan_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        
    def test_get_show_plan_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)