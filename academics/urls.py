from django.urls import path
from . import views

app_name = "academics"

urlpatterns = [
    path("", views.academic_structure_home, name="home"),

    path("departments/", views.department_list, name="department_list"),
    path("departments/<int:pk>/edit/", views.department_update, name="department_update"),
    path("departments/<int:pk>/delete/", views.department_delete, name="department_delete"),

    path("programmes/", views.programme_list, name="programme_list"),
    path("programmes/<int:pk>/edit/", views.programme_update, name="programme_update"),
    path("programmes/<int:pk>/delete/", views.programme_delete, name="programme_delete"),

    path("levels/", views.level_list, name="level_list"),
    path("levels/<int:pk>/edit/", views.level_update, name="level_update"),
    path("levels/<int:pk>/delete/", views.level_delete, name="level_delete"),

    path("courses/", views.course_list, name="course_list"),
    path("courses/<int:pk>/edit/", views.course_update, name="course_update"),
    path("courses/<int:pk>/delete/", views.course_delete, name="course_delete"),

    path("curriculum/", views.curriculum_list, name="curriculum_list"),
    path("curriculum/<int:pk>/edit/", views.curriculum_update, name="curriculum_update"),
    path("curriculum/<int:pk>/delete/", views.curriculum_delete, name="curriculum_delete"),

    path("sessions/", views.session_list, name="session_list"),
    path("sessions/<int:pk>/edit/", views.session_update, name="session_update"),
    path("sessions/<int:pk>/delete/", views.session_delete, name="session_delete"),
    path("sessions/<int:pk>/set-current/", views.session_set_current, name="session_set_current"),
    path("semesters/<int:pk>/set-current/", views.semester_set_current, name="semester_set_current"),
]




