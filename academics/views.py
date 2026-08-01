from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.decorators import admin_required
from .models import Department, Programme, Level, Session, Semester, Course, Curriculum
from .forms import DepartmentForm, CourseForm, CurriculumForm


@login_required
@admin_required
def academic_structure_home(request):
    context = {
        "departments": Department.objects.all(),
        "programmes": Programme.objects.all(),
        "sessions": Session.objects.all(),
        "courses_count": Course.objects.count(),
    }
    return render(request, "academics/structure_home.html", context)


@login_required
@admin_required
def department_list(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department created.")
            return redirect("academics:department_list")
    else:
        form = DepartmentForm()

    departments = Department.objects.all()
    return render(request, "academics/department_list.html", {"departments": departments, "form": form})


@login_required
@admin_required
def course_list(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Course created.")
            return redirect("academics:course_list")
    else:
        form = CourseForm()

    courses = Course.objects.select_related("department").all()
    return render(request, "academics/course_list.html", {"courses": courses, "form": form})


@login_required
@admin_required
def curriculum_list(request):
    if request.method == "POST":
        form = CurriculumForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Curriculum entry added.")
            return redirect("academics:curriculum_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CurriculumForm()

    curriculum_entries = Curriculum.objects.select_related(
        "course", "department", "programme", "level"
    ).all()
    return render(request, "academics/curriculum_list.html", {
        "curriculum_entries": curriculum_entries,
        "form": form,
    })


@login_required
@admin_required
def curriculum_delete(request, pk):
    entry = get_object_or_404(Curriculum, pk=pk)
    entry.delete()
    messages.success(request, "Curriculum entry removed.")
    return redirect("academics:curriculum_list")








