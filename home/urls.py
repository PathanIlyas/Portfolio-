from django.urls import path
from . import views

urlpatterns = [
    # Public route
    path("", views.index, name="index"),
    path("about/", views.about_view, name="about"),
    path("expertise/", views.expertise_view, name="expertise"),
    path("projects/", views.projects_view, name="projects"),
    path("contact/", views.contact_view, name="contact"),
    
    # Authentication routes
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("client/register/", views.client_register, name="client_register"),
    path("client/login/", views.client_login, name="client_login"),
    
    # Dashboard routes (CRUD)
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/add/", views.project_add, name="project_add"),
    path("dashboard/edit/<int:pk>/", views.project_edit, name="project_edit"),
    path("dashboard/delete/<int:pk>/", views.project_delete, name="project_delete"),
    
    # Dashboard - Skills CRUD
    path("dashboard/skills/", views.skill_list, name="skill_list"),
    path("dashboard/skills/add/", views.skill_add, name="skill_add"),
    path("dashboard/skills/edit/<int:pk>/", views.skill_edit, name="skill_edit"),
    path("dashboard/skills/delete/<int:pk>/", views.skill_delete, name="skill_delete"),
    
    # Dashboard - Profile Edit
    path("dashboard/profile/", views.profile_edit, name="profile_edit"),
    
    # Dashboard - Messages Inbox
    path("dashboard/messages/", views.message_list, name="message_list"),
    path("dashboard/messages/<int:pk>/", views.message_detail, name="message_detail"),
    path("dashboard/messages/delete/<int:pk>/", views.message_delete, name="message_delete"),
]
