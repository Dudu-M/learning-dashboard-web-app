from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.views.generic.edit import UpdateView, DeleteView
from..forms import ReflectionForm
from ..models import Plan, Reflection

@login_required
def reflection(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    context = {"plan": plan, "form": ReflectionForm()}
    if request.method == 'POST':
        form = ReflectionForm(request.POST)
        if form.is_valid():
            form.save(plan)
            messages.success(request, 'Reflection saved successfully')
            return redirect('show_plan', plan.id)
        else:
            messages.error(request, 'There was an issue saving your reflection')
            return render(request, 'reflection.html', {"plan": plan, "form": form})
    else:
        return render(request, 'reflection.html', context)
    
@login_required
def reflection_list(request):
    plans = request.user.plans.all().order_by('-id')
    reflections = [p.get_reflection()[0] for p in plans if p.has_reflection()]
    return render(request, 'reflections_list.html', {"reflections": reflections})

class ReflectionEditView(LoginRequiredMixin, UpdateView):
    """View to update reflection"""

    model = Reflection
    template_name = "reflection_edit.html"
    fields = ["time_reflection", "study_method_reflection", "carry_forward_reflection"]
    
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().plan_reflection not in request.user.plans.all():
            messages.add_message(self.request, messages.ERROR, "Not a valid Reflection to edit")
            return redirect(reverse('plans_list'))
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plan"] = self.get_object().plan_reflection
        return context

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.add_message(self.request, messages.SUCCESS, "Reflection updated!")
        return reverse('show_plan', kwargs={'plan_id': self.get_object().plan_reflection.id})

class ReflectionDeleteView(LoginRequiredMixin, DeleteView):
    model = Reflection
    http_method_names = ['delete']

    def dispatch(self, request, *args, **kwargs):
        # safety checks is user allowed to delete?
        if self.get_object().plan_reflection not in request.user.plans.all():
            messages.add_message(self.request, messages.ERROR, "Not a valid Reflection to delete")
            return HttpResponseForbidden()
        else:
            handler = getattr(self, 'delete')
            return handler(request, *args, **kwargs)
        
    def get_success_url(self):
        """Return redirect URL after successful delete."""
        messages.add_message(self.request, messages.SUCCESS, "Reflection deleted successfully!")
        return reverse('show_plan', kwargs={'plan_id': self.get_object().plan_reflection.id})