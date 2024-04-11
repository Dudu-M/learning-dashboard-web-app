""""Unit tests of Plan Model"""
from django.core.exceptions import ValidationError
from django.test import TestCase
from polls.models import Plan

class UserTestCase(TestCase):
    fixtures = [
        'polls/tests/fixtures/plans.json',
    ]  
    def setUp(self):
        self.plan = Plan.objects.get(id=1)
        
    def test_valid_plan(self):
        self._assert_plan_is_valid()
        
    # week tests
    def test_plan_week_must_be_from_pre_set_list(self):
        self.plan.week_plan = "WEEK Z"
        self._assert_plan_is_invalid()
        
    # time_plan
    def test_time_plan_cannot_be_blank(self):
        self.plan.time_plan = ''
        self._assert_plan_is_invalid()
        
    def test_time_plan_can_be_4000_characters_long(self):
        self.plan.time_plan = 'x' * 4000
        self._assert_plan_is_valid()

    def test_time_plan_cannot_be_over_4000_characters_long(self):
        self.plan.time_plan = 'x' * 4001
        self._assert_plan_is_invalid()
        
    # study_method
    def test_study_method_cannot_be_blank(self):
        self.plan.study_method = ''
        self._assert_plan_is_invalid()
        
    def test_study_method_can_be_4000_characters_long(self):
        self.plan.study_method = 'x' * 4000
        self._assert_plan_is_valid()

    def test_study_method_cannot_be_over_4000_characters_long(self):
        self.plan.study_method = 'x' * 4001
        self._assert_plan_is_invalid()

    # assertion helpers
    def _assert_plan_is_valid(self):
        try:
            self.plan.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_plan_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.plan.full_clean()