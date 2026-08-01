from django.urls import path
from . import views

app_name = "lecturers"

urlpatterns = [
    path("register/", views.register_lecturer, name="register_lecturer"),
    path("", views.lecturer_list, name="lecturer_list"),
    path("allocate/", views.allocate_course, name="allocate_course"),
    path("allocations/", views.allocation_list, name="allocation_list"),
    path("allocations/<int:pk>/delete/", views.allocation_delete, name="allocation_delete"),
    path("dashboard/", views.lecturer_dashboard, name="dashboard"),
]



