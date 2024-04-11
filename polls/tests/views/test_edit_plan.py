"""Unit tests for the PlanEdit view."""
from django.test import TestCase
from django.urls import reverse
from polls.models import User, Plan
from polls.tests.helpers import reverse_with_next

class PlanEditViewTestCase(TestCase):
    fixtures = [
        'polls/tests/fixtures/users.json',
        'polls/tests/fixtures/plans.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='JaneID123')
        self.plan = Plan.objects.get(id = 1)
        self.user.plans.add(self.plan)
        self.url = reverse('plan_edit', kwargs={'pk': self.plan.id})
        
    def test_plan_edit_url(self):
        self.assertEqual(self.url, f'/polls/plan_edit/{self.plan.id}')

    def test_get_plan_edit(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_plan.html')
        
    def test_get_plan_edit_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        
    def test_editing_plan_does_not_create_increase_count(self):
        pass
    
    def test_cannot_edit_non_other_student_plan(self):
        pass
        self.client.login(username=self.user.username, password='Password123')
        self.url = reverse('plan_edit', kwargs={'pk': 2})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)