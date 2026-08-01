from django.urls import path
from . import views

app_name = "results"

urlpatterns = [
    path("select-course/", views.select_course_for_entry, name="select_course"),
    path("enter/<int:allocation_id>/", views.enter_results, name="enter_results"),
    path("my-results/", views.view_results, name="view_results"),
    path("admin/", views.admin_result_list, name="admin_result_list"),
    path("admin/publish/", views.publish_results, name="publish_results"),
]
