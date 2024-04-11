"""Forms for the polls app."""
from django import forms
from django.forms import Textarea
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Plan, Reflection

class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def get_user(self):
        """Returns authenticated user if possible."""

        user = None
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
        return user
    
class SignUpForm(forms.Form):
    """Form enabling unregistered users to sign up."""

    username = forms.CharField(label = "StudentID", max_length = 50)
    
    new_password = forms.CharField(
        label = 'Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message ='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        # check if studentID is valid
        try:
            username = self.cleaned_data.get('username')
            if not username:
                self.add_error('username',"Username must not be blank")
            user = User.objects.get(username = username)
            if user is None:
                self.add_error('username',"Invalid StudentID. Try again.")
            else:
                if user.has_usable_password():
                    self.add_error('username',"Account for this StudentID exists. Try Log In instead.")
        except ObjectDoesNotExist:
            self.add_error('username',"Student ID does not exist. Try again.")
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')

    def save(self):
        """Save password to user account."""
        
        self.is_valid()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('new_password')
        
        user = User.objects.get(username = username)
        user.set_password(password)
        user.save() 
        return user
    
    
class PlanForm(forms.ModelForm):
    """Form enabling users to plan for a specific academic week."""

    class Meta:
        """Form options."""

        model = Plan
        fields = ['week_plan', 'time_plan', 'study_method']
        widgets = {
            "study_method": Textarea(attrs={"cols": 80, "rows": 5}),
            "time_plan": Textarea(attrs={"cols": 80, "rows": 3}),
        }
        labels = {
            "week_plan": _("Week"),
            "study_method": mark_safe('How do you plan to study for this week? <a href="https://www.ilovepdf.com/blog/best-study-methods-techniques" target="_blank" style="text-decoration:none"><br><i>study method ideas</a></i>.'),
        }
        help_texts = {
            "time_plan": _("How long do you plan to spend studying each module"),
        }
        
    def save(self):
        """Create a new plan."""

        super().save(commit=False)
        plan = Plan.objects.get_or_create(
            week_plan = self.cleaned_data.get('week_plan'),
            time_plan = self.cleaned_data.get('time_plan'),
            study_method = self.cleaned_data.get('study_method'),
        )
        return plan
    
class ReflectionForm(forms.ModelForm):
    """Form enabling users to reflect on previously set plans."""

    class Meta:
        """Form options."""

        model = Reflection
        fields = ['time_reflection', 'study_method_reflection','carry_forward_reflection' ]
        widgets = {
            "time_reflection": Textarea(attrs={"cols": 80, "rows": 3}),
            "study_method_reflection": Textarea(attrs={"cols": 80, "rows":7}),
            "carry_forward_reflection": Textarea(attrs={"cols": 80, "rows": 4}),
        }
        labels = {
            "time_reflection": _("How long did you actually study?"),
            "study_method_reflection": _("Did you follow your plan? Think about what worked well and what didn't"),
            "carry_forward_reflection": _("What did you learn and will carry forward?"),
        }
        
    def save(self, plan):
        """Create a new plan."""

        super().save(commit=False)
        reflection = Reflection.objects.update_or_create(
            plan_reflection = plan,
            time_reflection = self.cleaned_data.get('time_reflection'),
            study_method_reflection = self.cleaned_data.get('study_method_reflection'),
            carry_forward_reflection = self.cleaned_data.get('carry_forward_reflection'),
        )
        return reflection