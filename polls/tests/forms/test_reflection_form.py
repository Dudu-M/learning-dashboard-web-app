"""Unit tests of the Reflection Form."""
from django import forms
from django.test import TestCase
from polls.forms import ReflectionForm

class ReflectionFormTestCase(TestCase):

    fixtures = ['polls/tests/fixtures/reflections.json',
                'polls/tests/fixtures/plans.json'
                ]

    def setUp(self):
        self.form_input = {
            'time_reflection': 'Lorem ipsum dolor sit amet', 
            'study_method_reflection': 'Lorem ipsum dolor sit amet, consectetur adipiscing',
            'carry_forward_reflection': 'Lorem ipsum dolor sit amet, consectetur adipiscing'}

    def test_form_contains_required_fields(self):
        form = ReflectionForm()
        self.assertIn('time_reflection', form.fields)
        self.assertIn('study_method_reflection', form.fields)
        
        time_reflection_field = form.fields['time_reflection']
        study_method_reflection_field = form.fields['study_method_reflection']
        carry_forward_reflection_field = form.fields['carry_forward_reflection']
        
        self.assertTrue(isinstance(time_reflection_field, forms.CharField))
        self.assertTrue(isinstance(study_method_reflection_field, forms.CharField))
        self.assertTrue(isinstance(carry_forward_reflection_field, forms.CharField))
        
    def test_form_accepts_valid_input(self):
        form = ReflectionForm(data = self.form_input)
        self.assertTrue(form.is_valid())
        
    def test_form_does_not_accept_blank_time_reflection(self):
        self.form_input['time_reflection'] = ''
        form = ReflectionForm(data = self.form_input)
        self.assertFalse(form.is_valid())
        
    def test_form_does_not_accept_blank_study_method_reflection(self):
        self.form_input['study_method_reflection'] = ''
        form = ReflectionForm(data = self.form_input)
        self.assertFalse(form.is_valid())
        
    def test_form_does_not_accept_blank_carry_forward_reflection(self):
        self.form_input['carry_forward_reflection'] = ''
        form = ReflectionForm(data = self.form_input)
        self.assertFalse(form.is_valid())