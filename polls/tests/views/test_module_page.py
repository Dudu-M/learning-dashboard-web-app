"""Unit tests for the Module Page view."""
from django.test import TestCase
from django.urls import reverse
from polls.models import User, Module
from polls.tests.helpers import reverse_with_next

class ModulePageViewTestCase(TestCase):
    fixtures = [
        'polls/tests/fixtures/users.json',
        'polls/tests/fixtures/modules.json',
        'polls/tests/fixtures/resources.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='JaneID123')
        self.module = Module.objects.get(id = 1)
        self.user.modules.add(self.module)
        self.url = reverse('module_page', kwargs={'module_code': self.module.module_code})
        
    def test_module_page_url(self):
        self.assertEqual(self.url, f'/polls/module/{self.module.module_code}')

    def test_get_module_page(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'module_page.html')
        
    def test_get_module_page_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        
    def test_get_module_page_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)