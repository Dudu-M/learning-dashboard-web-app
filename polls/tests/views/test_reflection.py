"""Unit tests for the Reflection view."""
from django.test import TestCase
from django.urls import reverse
from polls.models import User, Plan, Reflection
from polls.tests.helpers import reverse_with_next

class ReflectionViewTestCase(TestCase):
    fixtures = [
        'polls/tests/fixtures/users.json',
        'polls/tests/fixtures/plans.json',
        'polls/tests/fixtures/reflections.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='JaneID123')
        self.plan = Plan.objects.get(id = 1)
        self.url = reverse('reflection', kwargs={'plan_id': self.plan.id})
        
    def test_reflection_url(self):
        self.assertEqual(self.url, f'/polls/reflection/{self.plan.id}')

    def test_get_reflection(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reflection.html')
        
    def test_get_reflection_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        
    def test_get_reflection_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)