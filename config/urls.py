from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path("django-admin/", admin.site.urls),  # Django's built-in admin, kept separate from app "admin" role

    path("", RedirectView.as_view(pattern_name="accounts:login", permanent=False)),

    path("accounts/", include("accounts.urls")),
    path("academics/", include("academics.urls")),
    path("students/", include("students.urls")),
    path("lecturers/", include("lecturers.urls")),
    path("results/", include("results.urls")),
    path("reports/", include("reports.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)