""""Unit tests of User Model"""
from django.core.exceptions import ValidationError
from django.test import TestCase
from polls.models import User, Plan, Module, Resource

class UserTestCase(TestCase):
    fixtures = [
        'polls/tests/fixtures/users.json',
        'polls/tests/fixtures/modules.json',
        'polls/tests/fixtures/resources.json',
        'polls/tests/fixtures/plans.json'
    ]  
    def setUp(self):
        self.user = User.objects.get(username='JaneID123')
        self.second_user = User.objects.get(username='JohnID123')
        self.module = Module.objects.get(id = 1)
        self.plan = Plan.objects.get(id=1)
        
    def test_valid_user(self):
        self._assert_user_is_valid()
        
    # username tests
    def test_username_cannot_be_blank(self):
        self.user.username = ''
        self._assert_user_is_invalid()

    def test_username_can_be_50_characters_long(self):
        self.user.username = 'x' * 50
        self._assert_user_is_valid()

    def test_username_cannot_be_over_50_characters_long(self):
        self.user.username = 'x' * 51
        self._assert_user_is_invalid()

    def test_username_must_be_unique(self):
        self.user.username = self.second_user.username
        self._assert_user_is_invalid()
        
    # first name tests
    def test_first_name_must_not_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()

    def test_first_name_need_not_be_unique(self):
        self.user.first_name = self.second_user.first_name
        self._assert_user_is_valid()

    def test_first_name_may_contain_50_characters(self):
        self.user.first_name = 'x' * 50
        self._assert_user_is_valid()

    def test_first_name_must_not_contain_more_than_50_characters(self):
        self.user.first_name = 'x' * 51
        self._assert_user_is_invalid()
        
    # last name tests
    def test_last_name_must_not_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()

    def test_last_name_need_not_be_unique(self):
        self.user.last_name = self.second_user.first_name
        self._assert_user_is_valid()

    def test_last_name_may_contain_50_characters(self):
        self.user.last_name = 'x' * 50
        self._assert_user_is_valid()

    def test_last_name_must_not_contain_more_than_50_characters(self):
        self.user.last_name = 'x' * 51
        self._assert_user_is_invalid()
        
    # email tests
    def test_email_must_not_be_blank(self):
        self.user.email = ''
        self._assert_user_is_invalid()

    def test_email_must_be_unique(self):
        self.user.email = self.second_user.email
        self._assert_user_is_invalid()

    def test_email_must_contain_at_symbol(self):
        self.user.email = 'jane.doe.example.com'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain_name(self):
        self.user.email = 'jane.doe@.com'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain(self):
        self.user.email = 'janedoe@example'
        self._assert_user_is_invalid()

    def test_email_must_not_contain_more_than_one_at(self):
        self.user.email = 'janedoe@@example.com'
        self._assert_user_is_invalid()
        
    # plans tests
    def test_creating_new_plan_increases_plans(self):
        plan = Plan.objects.get(id=1)
        self.assertEqual(self.user.plans.count(), 0)
        self.user.add_plan(plan)
        self.assertEqual(self.user.plans.count(), 1)
    
    # completed resources tests
    def test_completed_resources_increase_when_marked_complete(self):
        resources_ids =[1, 2]
        self.assertEqual(self.user.completed_resources.count(), 0)
        self.user.adjust_completed_resources(resources_ids, self.module)
        self.assertEqual(self.user.completed_resources.count(), 2)
        
    def test_completed_resources_decrease_when_unmarked_complete(self):
        resources_ids =[1, 2]
        self.assertEqual(self.user.completed_resources.count(), 0)
        self.user.adjust_completed_resources(resources_ids, self.module)
        self.assertEqual(self.user.completed_resources.count(), 2)
        resources_ids =[1]
        self.user.adjust_completed_resources(resources_ids, self.module)
        self.assertEqual(self.user.completed_resources.count(), 1)
    
    # assertion helpers
    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()
