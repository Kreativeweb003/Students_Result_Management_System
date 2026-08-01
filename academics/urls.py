from django.urls import path
from . import views

app_name = "academics"

urlpatterns = [
    path("", views.academic_structure_home, name="home"),
    path("departments/", views.department_list, name="department_list"),
    path("courses/", views.course_list, name="course_list"),
    path("curriculum/", views.curriculum_list, name="curriculum_list"),
    path("curriculum/<int:pk>/delete/", views.curriculum_delete, name="curriculum_delete"),
]


