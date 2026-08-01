from django.contrib import admin
from .models import Lecturer, CourseAllocation


@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ("staff_id", "full_name", "department", "title")
    list_filter = ("department",)
    search_fields = ("staff_id", "user__first_name", "user__last_name", "user__username")

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = "Name"


@admin.register(CourseAllocation)
class CourseAllocationAdmin(admin.ModelAdmin):
    list_display = ("lecturer", "course", "session", "semester")
    list_filter = ("session", "semester", "course__department")
    search_fields = ("lecturer__staff_id", "lecturer__user__last_name", "course__code")








