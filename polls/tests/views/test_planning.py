"""Unit tests for the Plan Creation view."""
from django.test import TestCase
from django.urls import reverse
from polls.models import User, Plan
from polls.tests.helpers import reverse_with_next

class PlanningViewTestCase(TestCase):
    fixtures = [
        'polls/tests/fixtures/users.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='JaneID123')
        self.input = {
            'week_plan': 'WEEK 1', 
            'time_plan': 'Lorem ipsum dolor sit amet', 
            'study_method': 'Lorem ipsum dolor sit amet, consectetur adipiscing'}
        self.url = reverse('planning')
        
    def test_planning_url(self):
        self.assertEqual(self.url, '/polls/planning/')
        

    def test_get_overview(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planning.html')
        
    def test_get_plannning_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        
    def test_get_planning_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)