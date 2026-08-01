from django.contrib import admin
from .models import Department, Programme, Level, Session, Semester, Course, Curriculum


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ("programme", "name")
    list_filter = ("programme",)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("name", "is_current")
    list_filter = ("is_current",)


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("session", "name", "is_current")
    list_filter = ("session", "is_current")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "unit", "department")
    list_filter = ("department",)
    search_fields = ("code", "title")


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ("course", "department", "programme", "level", "semester_name")
    list_filter = ("department", "programme", "level", "semester_name")
    search_fields = ("course__code", "course__title")






