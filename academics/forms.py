from django import forms
from .models import Department, Programme, Level, Session, Semester, Course, Curriculum


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "code"]


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["code", "title", "unit", "department"]


class CurriculumForm(forms.ModelForm):
    class Meta:
        model = Curriculum
        fields = ["department", "programme", "level", "semester_name", "course"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # narrow course choices to the selected department, if provided via initial/bound data
        department_id = self.data.get("department") or self.initial.get("department")
        if department_id:
            self.fields["course"].queryset = Course.objects.filter(department_id=department_id)






