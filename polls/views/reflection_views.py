from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from..forms import ReflectionForm
from ..models import Plan

@login_required
def reflection(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    context = {"plan": plan, "form": ReflectionForm()}
    if request.method == 'POST':
        form = ReflectionForm(request.POST)
        if form.is_valid():
            form.save(plan)
            messages.success(request, 'Reflection saved successfully')
            return redirect('plans_list')
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