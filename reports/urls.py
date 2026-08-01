from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("slip/<int:session_id>/<int:semester_id>/", views.download_result_slip, name="result_slip"),
    path("transcript/", views.download_transcript, name="transcript"),
    path("statistics/", views.department_statistics, name="statistics"),
]
