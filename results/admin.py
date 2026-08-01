from django.contrib import admin
from .models import GradingScale, Result


@admin.register(GradingScale)
class GradingScaleAdmin(admin.ModelAdmin):
    list_display = ("grade", "min_score", "max_score", "grade_point")
    ordering = ("-min_score",)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "session", "semester", "total_score", "grade", "is_published")
    list_filter = ("session", "semester", "course__department", "is_published")
    search_fields = ("student__matric_number", "course__code")
    actions = ["publish_results", "unpublish_results"]

    def publish_results(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f"{updated} result(s) published.")
    publish_results.short_description = "Publish selected results"

    def unpublish_results(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f"{updated} result(s) unpublished.")
    unpublish_results.short_description = "Unpublish selected results"
  