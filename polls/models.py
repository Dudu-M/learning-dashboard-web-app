from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# Create your models here.
class Module(models.Model):
    module_code = models.CharField(max_length = 20, unique=True)
    module_name = models.CharField(max_length = 200)
    
    def __str__(self):
        return self.module_code + " " + self.module_name
    
# specifying the choices of resource types
RESOURCE_TYPES = (
    ("VIDEO", "Video"),
    ("DOCUMENT", "Document"),
    ("READING", "Reading"),
    ("ARTICLE", "Article"),
    ("OTHER", "Other"),
)

# specifying the importance of resources
RESOURCE_IMPORTANCE = (
    ("MANDATORY", "Mandatory"),
    ("RECOMMENDED", "Recommended"),
    ("OPTIONAL", "Optional"),
)

# specifying the importance of resources
RESOURCE_WEEK = (
    ("WEEK 1", "Week 1"),
    ("WEEK 2", "Week 2"),
    ("WEEK 3", "Week 3"),
    ("WEEK 4", "Week 4"),
    ("WEEK 5", "Week 5"),
)

class Resource(models.Model):
    module = models.ForeignKey(Module, on_delete = models.CASCADE)
    resource_name = models.CharField(max_length = 200)
    resource_type = models.CharField(max_length = 20, choices = RESOURCE_TYPES)
    recommended_time_in_minutes = models.IntegerField()
    importance = models.CharField(max_length = 20, choices = RESOURCE_IMPORTANCE, default = 'MANDATORY')
    scheduled_week = models.CharField(max_length = 20, choices = RESOURCE_WEEK)
    
    
    def __str__(self):
        return self.module.module_code + "_" + self.resource_name

class Plan(models.Model):
    week_plan = models.CharField(max_length = 20, choices = RESOURCE_WEEK)
    # module_plan = models.ForeignKey(Module, on_delete = models.CASCADE)
    time_plan = models.CharField(max_length = 4000, blank = False)
    study_method = models.CharField(max_length = 4000, blank = False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Model options."""

        ordering = ['-created_at']
    
    def get_reflection(self):
        reflections=Reflection.objects.filter(plan_reflection=self)
        return reflections
    
    def has_reflection(self):
        return len(self.get_reflection())>0
    
    def get_days_to_reflection(self):
        today = datetime.date.today()
        days = (self.get_reflection_date()-today).days
        return days
    
    def get_reflection_date(self):
        target_date = (self.created_at + datetime.timedelta(days=1)).date()
        return target_date
    
    def reflection_overdue(self):
        return (not self.has_reflection()) and self.get_days_to_reflection()<=0
    
class Reflection(models.Model):
    plan_reflection = models.ForeignKey(Plan, on_delete = models.CASCADE)
    time_reflection = models.CharField(max_length = 4000, blank = False)
    study_method_reflection = models.CharField(max_length = 4000, blank = False)
    carry_forward_reflection = models.CharField(max_length = 4000, blank = False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        """Model options."""

        ordering = ['-created_at']
    
class User(AbstractUser):
    username = models.CharField(unique = True, max_length = 50, blank = False)
    first_name = models.CharField(max_length = 50, blank = False)
    last_name = models.CharField(max_length = 50, blank = False)
    email = models.EmailField(max_length=254, unique = True)
    modules = models.ManyToManyField(Module)
    plans = models.ManyToManyField(Plan, blank = True)
    completed_resources = models.ManyToManyField(Resource, blank = True)
    
    def add_plan(self, plan):
        self.plans.add(plan)
        
    # add or remove completed resources according to passed list
    def adjust_completed_resources(self, complete_r_ids, module):
        completed_resources = Resource.objects.filter(id__in = complete_r_ids)
        updated_r = self.completed_resources.exclude(module=module).union(completed_resources)
        self.completed_resources.set(updated_r)
        
    #returns users latest reflection
    def last_reflection(self):
        if self.plans:
            reflections = Reflection.objects.none()
            for p in self.plans.all():
                if p.has_reflection():
                    reflections = (reflections | p.get_reflection())
            reflections = Reflection.objects.filter(id__in = reflections)
            return  reflections.latest('created_at')
        return None
    
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []
    
