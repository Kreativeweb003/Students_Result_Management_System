from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("matric_number", "full_name", "department", "programme", "level", "study_mode")
    list_filter = ("department", "programme", "level", "study_mode", "gender")
    search_fields = ("matric_number", "user__first_name", "user__last_name", "user__email")
    readonly_fields = ("matric_number",)

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = "Name"







