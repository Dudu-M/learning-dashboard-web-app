""""Unit tests of Resource Model"""
from django.core.exceptions import ValidationError
from django.test import TestCase
from polls.models import Resource

class UserTestCase(TestCase):
    fixtures = [
        'polls/tests/fixtures/resources.json',
        'polls/tests/fixtures/modules.json',
    ]  
    def setUp(self):
        self.resource = Resource.objects.get(id=1)
        
    def test_valid_resource(self):
        self._assert_resource_is_valid()

    # module tests
    def test_module_cannot_be_blank(self):
        self.resource.module = None
        self._assert_resource_is_invalid()
        
    # resource_name tests
    def test_resource_name_can_be_200_characters_long(self):
        self.resource.resource_name = 'x' * 200
        self._assert_resource_is_valid()

    def test_resource_name_cannot_be_over_200_characters_long(self):
        self.resource.resource_name = 'x' * 201
        self._assert_resource_is_invalid()
        
    # recommended_time tests
    def test_time_must_be_an_integer(self):
        self.resource.recommended_time_in_minutes = "String"
        self._assert_resource_is_invalid()
        
    # importance tests
    def test_importance_must_be_from_pre_set_list(self):
        self.resource.importance = "NOT IN LIST"
        self._assert_resource_is_invalid()
        
    # scheduled_week tests
    def test_scheduled_week_must_be_from_pre_set_list(self):
        self.resource.scheduled_week = "WEEK Z"
        self._assert_resource_is_invalid()

    # assertion helpers
    def _assert_resource_is_valid(self):
        try:
            self.resource.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_resource_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.resource.full_clean()