from django.urls import path
from . import views

app_name = "examoffice"

urlpatterns = [
    path("register/", views.register_exam_officer, name="register_officer"),
    path("officers/", views.officer_list, name="officer_list"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("students/<int:pk>/results/", views.student_results, name="student_results"),

    path("pending/", views.pending_results, name="pending_results"),
    path("pending/approve-all/", views.approve_all_pending, name="approve_all_pending"),
    path("reject/<int:pk>/", views.reject_result, name="reject_result"),
]

