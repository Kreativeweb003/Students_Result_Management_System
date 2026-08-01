from django.urls import path
from . import views

app_name = "students"

urlpatterns = [
    path("register/", views.register_student, name="register_student"),
    path("", views.student_list, name="student_list"),
    path("<int:pk>/", views.student_detail, name="student_detail"),
    path("dashboard/", views.student_dashboard, name="dashboard"),
    path("profile/", views.student_profile, name="profile"),
]




