""""Unit tests of Reflection Model"""
from django.core.exceptions import ValidationError
from django.test import TestCase
from polls.models import Plan, Reflection

class UserTestCase(TestCase):
    fixtures = [
        'polls/tests/fixtures/reflections.json',
        'polls/tests/fixtures/plans.json'
    ]  
    def setUp(self):
        self.reflection = Reflection.objects.get(id=1)
        
    def test_valid_reflection(self):
        self._assert_reflection_is_valid()
        
    # plan
    def plan_cannot_not_blank(self):
        self.reflection.plan_reflection = None
        self._assert_reflection_is_invalid()
        
    # time_reflection
    def test_time_reflection_cannot_be_blank(self):
        self.reflection.time_reflection = ''
        self._assert_reflection_is_invalid()
        
    def test_time_reflection_can_be_4000_characters_long(self):
        self.reflection.time_reflection = 'x' * 4000
        self._assert_reflection_is_valid()

    def test_time_reflection_cannot_be_over_4000_characters_long(self):
        self.reflection.time_reflection = 'x' * 4001
        self._assert_reflection_is_invalid()
        
    # study_method
    def test_study_method_cannot_be_blank(self):
        self.reflection.study_method_reflection = ''
        self._assert_reflection_is_invalid()
        
    def test_study_method_can_be_4000_characters_long(self):
        self.reflection.study_method_reflection = 'x' * 4000
        self._assert_reflection_is_valid()

    def test_study_method_cannot_be_over_4000_characters_long(self):
        self.reflection.study_method_reflection = 'x' * 4001
        self._assert_reflection_is_invalid()
        
    # carry_forward_reflection
    def test_carry_forward_reflection_cannot_be_blank(self):
        self.reflection.carry_forward_reflection = ''
        self._assert_reflection_is_invalid()
        
    def test_carry_forward_reflection_can_be_4000_characters_long(self):
        self.reflection.carry_forward_reflection = 'x' * 4000
        self._assert_reflection_is_valid()

    def test_carry_forward_reflection_cannot_be_over_4000_characters_long(self):
        self.reflection.carry_forward_reflection = 'x' * 4001
        self._assert_reflection_is_invalid()

    # assertion helpers
    def _assert_reflection_is_valid(self):
        try:
            self.reflection.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_reflection_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.reflection.full_clean()