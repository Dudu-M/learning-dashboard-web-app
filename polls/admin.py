from django.contrib import admin

# Register your models here.
from .models import Module, Resource, User, Plan, Reflection

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for modules."""

    list_display = [
        'module_code', 'module_name',
    ]

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for resources."""

    list_display = [
        'module', 'resource_name', 'resource_type','scheduled_week', 'recommended_time_in_minutes',
    ]

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    list_display = [
        'first_name', 'last_name', 'email',
    ]
    
@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for plans."""

    list_display = [
        'week_plan', 'time_plan', 'study_method', 'created_at',
    ]
    
@admin.register(Reflection)
class ReflectionAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for reflections."""

    list_display = [
        'plan_reflection', 'time_reflection', 'study_method_reflection','carry_forward_reflection'
    ]