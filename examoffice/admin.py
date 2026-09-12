from django.contrib import admin
from .models import ExamOfficer


@admin.register(ExamOfficer)
class ExamOfficerAdmin(admin.ModelAdmin):
    list_display = ("staff_id", "full_name", "department")
    list_filter = ("department",)
    search_fields = ("staff_id", "user__first_name", "user__last_name")

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = "Name"