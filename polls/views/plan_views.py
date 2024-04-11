from..forms import PlanForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.decorators import login_required
from ..models import Plan
from django.shortcuts import render

class PlanningView(LoginRequiredMixin, FormView):
    """View that allows user to plan."""

    form_class = PlanForm
    template_name = "planning.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        self.request.user.add_plan(self.object[0])
        messages.add_message(self.request, messages.SUCCESS, "Plan created!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)
    
@login_required
def plans_list(request):
    plans = request.user.plans.all().order_by('-id')
    overdue = len([p for p in plans if p.reflection_overdue()])
    return render(request, 'plans_list.html', {"plans": plans, "form":PlanForm, "overdue":overdue})

@login_required
def show_plan(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    reflection = None
    if plan.has_reflection():
        reflection = plan.get_reflection()[0]
    print(reflection)
    return render(request, 'show_plan.html', {"plan": plan, "reflection": reflection})

class PlanEditView(LoginRequiredMixin, UpdateView):
    """View to update plan"""

    model = Plan
    template_name = "edit_plan.html"
    form_class = PlanForm

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.add_message(self.request, messages.SUCCESS, "Plan updated!")
        print(self.get_object())
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)