"""Unit tests of the Plan Form."""
from django import forms
from django.test import TestCase
from polls.forms import PlanForm

class PlanFormTestCase(TestCase):

    fixtures = ['polls/tests/fixtures/plans.json']

    def setUp(self):
        self.form_input = {
            'week_plan': 'WEEK 1', 
            'time_plan': 'Lorem ipsum dolor sit amet', 
            'study_method': 'Lorem ipsum dolor sit amet, consectetur adipiscing'}

    def test_form_contains_required_fields(self):
        form = PlanForm()
        self.assertIn('week_plan', form.fields)
        self.assertIn('time_plan', form.fields)
        self.assertIn('study_method', form.fields)
        week_plan_field = form.fields['week_plan']
        time_plan_field = form.fields['time_plan']
        study_method_field = form.fields['study_method']
        self.assertTrue(isinstance(week_plan_field,forms.ChoiceField))
        self.assertTrue(isinstance(time_plan_field, forms.CharField))
        self.assertTrue(isinstance(study_method_field, forms.CharField))
        
    def test_form_accepts_valid_input(self):
        form = PlanForm(data = self.form_input)
        self.assertTrue(form.is_valid())
        
    def test_form_does_not_accept_blank_week(self):
        self.form_input['week_plan'] = ''
        form = PlanForm(data = self.form_input)
        self.assertFalse(form.is_valid())
        
    def test_form_does_not_accept_blank_time_plan(self):
        self.form_input['time_plan'] = ''
        form = PlanForm(data = self.form_input)
        self.assertFalse(form.is_valid())
        
    def test_form_does_not_accept_blank_study_method(self):
        self.form_input['study_method'] = ''
        form = PlanForm(data = self.form_input)
        self.assertFalse(form.is_valid())