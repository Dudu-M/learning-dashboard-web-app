from django.urls import path
from .views import __int__ as views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('planning/', views.PlanningView.as_view(), name='planning'),
    path('plan_edit/<int:pk>', views.PlanEditView.as_view(), name='plan_edit'),
    path('overview/', views.overview, name='overview'),
    path('module/<str:module_code>', views.module_page, name='module_page'),
    path('reflection/<int:plan_id>', views.reflection, name='reflection'),
    path('plans/', views.plans_list, name='plans_list'),
    path('reflections/', views.reflection_list, name='reflection_list'),
    path('plan/<int:plan_id>', views.show_plan, name='show_plan'),
]