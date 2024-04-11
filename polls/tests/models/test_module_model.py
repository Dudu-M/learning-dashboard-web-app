""""Unit tests of Module Model"""
from django.core.exceptions import ValidationError
from django.test import TestCase
from polls.models import Module

class UserTestCase(TestCase):
    fixtures = [
        'polls/tests/fixtures/modules.json',
    ]  
    def setUp(self):
        self.module = Module.objects.get(id=1)
        self.second_module = Module.objects.get(id = 2)
        
    def test_valid_module(self):
        self._assert_module_is_valid()
        
    # module_code tests
    def test_module_code_must_be_unique(self):
        self.module.module_code = self.second_module.module_code
        self._assert_module_is_invalid()
        
    def test_module_code_can_be_20_characters_long(self):
        self.module.module_code = 'x' * 20
        self._assert_module_is_valid()

    def test_module_code_cannot_be_over_20_characters_long(self):
        self.module.module_code = 'x' * 21
        self._assert_module_is_invalid()
        
    # module_name tests
    def test_module_name_does_not_have_to_be_unique(self):
        self.module.module_name = self.second_module.module_name
        self._assert_module_is_valid()
        
    def test_module_name_can_be_200_characters_long(self):
        self.module.module_name = 'x' * 200
        self._assert_module_is_valid()

    def test_module_name_cannot_be_over_20_characters_long(self):
        self.module.module_name = 'x' * 201
        self._assert_module_is_invalid()

    # assertion helpers
    def _assert_module_is_valid(self):
        try:
            self.module.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_module_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.module.full_clean()