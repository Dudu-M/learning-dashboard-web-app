from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from..forms import PlanForm, ReflectionForm
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import ListView
from django.urls import reverse
from ..models import Resource, Module, Plan, Reflection
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count
import json
from django.db.models import Q


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@login_required 
def dashboard(request):
    user_modules = request.user.modules.all()
    user_resources = []
    current_plan = request.user.plans.first()
    if current_plan and current_plan.has_reflection():
        current_plan=None
    current_week = "Week_1" #use date to return the corresponding current date REMOVE
    for m in user_modules:
        user_resources += Resource.objects.filter(module=m)
    
    plans_reflections_due = [p for p in request.user.plans.all() if not p.has_reflection() and p.get_days_to_reflection() <=0 ]
    
    reflections_due = len(plans_reflections_due)
        
    context = {'user_modules': user_modules, 'user_resources': user_resources,
                'current_plan':current_plan, 'current_week': current_week, 'reflections_due': reflections_due }
    return render(request, 'dashboard.html',context )

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
def overview(request):
    if request.user.plans.exists() : 
        current_week = request.user.plans.first().week_plan
    else:
        current_week ="WEEK 1"
    week = current_week
    importance = "MANDATORY"
    completion_status = "all"
    if request.method == 'GET' and request.GET.get('selected_week', None):
        week = request.GET.get('selected_week', None)
        importance = request.GET.get('importance', None)
        completion_status = request.GET.get('complete', None)
    user=request.user
    modules = user.modules.all()
    labels = []
    data = []
    filtered_resources = []
    # week ->input value
    mandatory = []
    importances = set(Resource.objects.values_list("importance", flat=True).distinct().order_by("importance")) #!!!!
    importances.add("ALL")
    
    m_progress={}
    r_info = {}
    resource_type_labels = []
    resource_count_data = []
    weeks = list(Resource.objects.values_list("scheduled_week", flat=True).distinct().order_by("scheduled_week"))
    
    # user_modules = user.modules.all()
    # user_resources = Resource.objects.filter(module__in = user_modules, scheduled_week = week)
    # if not importance =='ALL':
    #     user_resources = user_resources.filter(importance = importance)
        
    # print (len(user_resources))
    for m in modules:
        labels.append(str(m))
        if not importance == "ALL":
            resources = Resource.objects.filter(module=m).filter(scheduled_week=week).filter(importance = importance)
        else:
            resources = Resource.objects.filter(module=m).filter(scheduled_week=week) # REFACTOR Resource.objects.filter(module_in=modules).filter(scheduled_week=week) 
            
        ur=user.completed_resources.filter(module=m).filter(scheduled_week=week)
        
        if completion_status == "incomplete":
            resources = resources.exclude(id__in = ur)
            
        if not importance =="ALL":
            ur= ur.filter(importance=importance)
            
        if resources:
            m_progress[m]=int(len(ur)/len(resources)*100) #.filter(importance = importance)
        else:
            m_progress[m]= 100
        
        module_resources=resources.values("resource_type").annotate(total=Sum("recommended_time_in_minutes"))
        filtered_resources+=resources.values_list("id", flat=True)
        ml = [ m["resource_type"] for m in module_resources]
        md = [m["total"] for m in module_resources]
        resource_type_labels.append(ml)
        resource_count_data.append(md)
        value = resources.aggregate(Sum("recommended_time_in_minutes", default=0)).get("recommended_time_in_minutes__sum")
        if value:
            data.append(round(value/60, 1)) 
        else:
            data.append(0) 
            
    r_types = []
    for rt in resource_type_labels: 
        r_types+=rt
    r_types = set(r_types)
    
    for rt in r_types:
        r_info[rt] = []
        
    for i in range(len(resource_type_labels)):
        for j in range(len(resource_type_labels[i])):
            rt = resource_type_labels[i][j]
            r = round(resource_count_data[i][j]/60, 1)
            r_info[rt].append(r)
            
        for d in r_info.items():
            if not len(d[1]) == i+1:
                r_info[d[0]].append(0)
    
    r_labels = list(r_info.keys())
    r_data = list(r_info.values())
    
    completed_selected_week = user.completed_resources.all().filter(id__in=filtered_resources)
    progress = 100
    if filtered_resources: 
        progress = int((len(completed_selected_week)/len(filtered_resources))*100)
        
    # print(progress)

    # plan_form = PlanForm(week_plan = week)
    # Plan form - week = week input
    # if plan for week exists - send form to be edited
    heaviest_module = labels[data.index(max(data))] + " ("+ minutes_to_hours_helper(max(data))+")"
    lightest_module = labels[data.index(min(data))] + " ("+ minutes_to_hours_helper(min(data))+")"
    total = minutes_to_hours_helper(sum(data))
    summary_data = {"Heaviest Module":  heaviest_module, "Total time estimated":total , "Lightest Module":lightest_module } #, "Mandatory Work": "[2.5hrs]"
    
    user_current_week_plans = user.plans.filter(week_plan=week)
    if user_current_week_plans:
        plan_form = PlanForm(instance=user_current_week_plans[0])
        plan = user_current_week_plans[0]
    else:
        plan = None
        plan_form = PlanForm()

    
    context = {"labels": labels, "data": data, "r_labels": json.dumps(r_labels), "r_data": json.dumps(r_data), "plan_form": plan_form, "plan" : plan, 
                "plans":user.plans, 'selected_week': week, 'completion_status': completion_status, 'weeks': weeks, "progress": progress, "summary_data":summary_data, 
                "importances":importances, "selected_importance":importance, "m_progress": m_progress, "time_total": round(sum(data),2)}

        
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            saved_form = form.save()
            user.add_plan(saved_form[0])
            messages.add_message(request, messages.SUCCESS, "Plan created!")
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            messages.add_message(request, messages.ERROR, "Error: Form invalid!")
            return render(request, 'overview.html', context)
    else:
        return render(request, 'overview.html', context)
    
@login_required
def module_page(request, module_code):
    module = Module.objects.get(module_code=module_code)
    module_resources = Resource.objects.filter(module=module)
    user = request.user
    # resources_by_week = {}
    resources_by_week = []
    completed_resources = request.user.completed_resources
    weeks = list(module_resources.values_list("scheduled_week", flat=True).distinct().order_by("scheduled_week"))
    for w in weeks:
        w_resources = module_resources.filter(scheduled_week = w)
        importances = list(w_resources.values_list("importance", flat=True).distinct().order_by("importance"))
        ur=completed_resources.filter(module=module).filter(scheduled_week=w).filter(importance="MANDATORY")        
        if w_resources.filter(importance="MANDATORY") :
            progress = int(len(ur)/len(w_resources.filter(importance="MANDATORY") )*100) #.filter(importance = importance)
        else:
            progress= 100
        resources_by_week.append((w,importances,w_resources, progress))

    # importances = list(module_resources.values_list("importance", flat=True).distinct().order_by("importance"))
    
    if request.method == 'POST':
        complete_r_ids = request.POST.getlist('checklist', None)
        user_cr_before = user.completed_resources
        # print(request.POST.getlist('checklist', None))
        if complete_r_ids:
            user.adjust_completed_resources(complete_r_ids, module)
        
    # relevant_completed = request.user.completed_resources.filter(module__in = module_resources)
    # print(relevant_completed)
    # user_completed_resources = [r for r in module_resources if r in request.user.completed_resources] 
    
    return render(request, 'module_page.html', {'module': module, 'module_resources': module_resources, 
                                                "resources_by_week": resources_by_week, "importances":importances })
# change to create reflection
@login_required
def reflection(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    context = {"plan": plan, "form": ReflectionForm()}
    if request.method == 'POST':
        form = ReflectionForm(request.POST)
        if form.is_valid():
            form.save(plan)
            messages.success(request, 'Reflection saved successfully')
            return redirect('plans_list') #change to list of previous plans and reflections
        else:
            return render(request, 'reflection.html', {"plan": plan, "form": form})
    else:
        return render(request, 'reflection.html', context)
    
    
def minutes_to_hours_helper(minutes):
    minutes = int(minutes*60)
    t = divmod(minutes, 60)
    if t[0] == 0:
        return str(t[1])+"mins"
    elif t[1] == 0:
        return str(t[0])+"hrs"
    else:
        return str(t[0])+"hrs " + str(t[1])+"mins"
    
@login_required
def reflection_list(request):
    plans = request.user.plans.all().order_by('-id')
    reflections = [p.get_reflection()[0] for p in plans if p.has_reflection()]
    return render(request, 'reflections_list.html', {"reflections": reflections})