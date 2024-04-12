from..forms import PlanForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from ..models import Plan
from django.shortcuts import render, redirect

class PlanningView(LoginRequiredMixin, FormView):
    """View that allows user to plan."""

    form_class = PlanForm
    template_name = "planning.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        self.request.user.add_plan(self.object)
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
    
    #prevent student to view plans that they dont own
    if plan not in request.user.plans.all() :
        messages.add_message(request, messages.ERROR, "Invalid Plan Access")
        return HttpResponseRedirect(reverse('plans_list'))

    reflection = None
    if plan.has_reflection():
        reflection = plan.get_reflection()[0]
    return render(request, 'show_plan.html', {"plan": plan, "reflection": reflection})

class PlanEditView(LoginRequiredMixin, UpdateView):
    """View to update plan"""

    model = Plan
    template_name = "edit_plan.html"
    fields = ["week_plan", "time_plan", "study_method"]
    
    def get_form(self, *args, **kwargs):
        form = super(PlanEditView, self).get_form(*args, **kwargs)
        form.fields["time_plan"].widget.attrs["class"] = "form-group"
        form.fields["study_method"].widget.attrs["class"] = "form-group"
        return form
    
    def dispatch(self, request, *args, **kwargs):
        if self.get_object() not in request.user.plans.all():
            messages.add_message(self.request, messages.ERROR, "Not a valid Plan to edit")
            return redirect(reverse('plans_list'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.add_message(self.request, messages.SUCCESS, "Plan updated!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)
    
class PlanDeleteView(LoginRequiredMixin, DeleteView):
    model = Plan
    http_method_names = ['delete']

    def dispatch(self, request, *args, **kwargs):
        # safety checks is user allowed to delete?
        if self.get_object() not in request.user.plans.all():
            messages.add_message(self.request, messages.ERROR, "Not a valid Plan to delete")
            return HttpResponseForbidden()
        else:
            handler = getattr(self, 'delete')
            return handler(request, *args, **kwargs)
        
    def get_success_url(self):
        """Return redirect URL after successful delete."""
        messages.add_message(self.request, messages.SUCCESS, "Plan deleted successfully!")
        return reverse('plans_list')