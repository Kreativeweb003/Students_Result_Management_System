from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.decorators import admin_required
from .models import Department, Programme, Level, Session, Semester, Course, Curriculum
from .forms import (
    DepartmentForm, ProgrammeForm, LevelForm, CourseForm, CurriculumForm, SessionForm,
)


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


# ---------------- Department ----------------

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
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated.")
            return redirect("academics:department_list")
    else:
        form = DepartmentForm(instance=department)

    return render(request, "academics/department_form.html", {"form": form, "department": department})


@login_required
@admin_required
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        try:
            department.delete()
            messages.success(request, "Department deleted.")
        except Exception:
            messages.error(
                request,
                "This department can't be deleted while it still has courses, students, "
                "or curriculum entries linked to it. Remove those first."
            )
    return redirect("academics:department_list")


# ---------------- Programme ----------------

@login_required
@admin_required
def programme_list(request):
    if request.method == "POST":
        form = ProgrammeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Programme created.")
            return redirect("academics:programme_list")
    else:
        form = ProgrammeForm()

    programmes = Programme.objects.all()
    return render(request, "academics/programme_list.html", {"programmes": programmes, "form": form})


@login_required
@admin_required
def programme_update(request, pk):
    programme = get_object_or_404(Programme, pk=pk)
    if request.method == "POST":
        form = ProgrammeForm(request.POST, instance=programme)
        if form.is_valid():
            form.save()
            messages.success(request, "Programme updated.")
            return redirect("academics:programme_list")
    else:
        form = ProgrammeForm(instance=programme)

    return render(request, "academics/programme_form.html", {"form": form, "programme": programme})


@login_required
@admin_required
def programme_delete(request, pk):
    programme = get_object_or_404(Programme, pk=pk)
    if request.method == "POST":
        try:
            programme.delete()
            messages.success(request, "Programme deleted.")
        except Exception:
            messages.error(
                request,
                "This programme can't be deleted while levels, students, or curriculum "
                "entries still reference it."
            )
    return redirect("academics:programme_list")


# ---------------- Level ----------------

@login_required
@admin_required
def level_list(request):
    if request.method == "POST":
        form = LevelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Level created.")
            return redirect("academics:level_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LevelForm()

    levels = Level.objects.select_related("programme").all()
    return render(request, "academics/level_list.html", {"levels": levels, "form": form})


@login_required
@admin_required
def level_update(request, pk):
    level = get_object_or_404(Level, pk=pk)
    if request.method == "POST":
        form = LevelForm(request.POST, instance=level)
        if form.is_valid():
            form.save()
            messages.success(request, "Level updated.")
            return redirect("academics:level_list")
    else:
        form = LevelForm(instance=level)

    return render(request, "academics/level_form.html", {"form": form, "level": level})


@login_required
@admin_required
def level_delete(request, pk):
    level = get_object_or_404(Level, pk=pk)
    if request.method == "POST":
        try:
            level.delete()
            messages.success(request, "Level deleted.")
        except Exception:
            messages.error(
                request,
                "This level can't be deleted while students or curriculum entries still reference it."
            )
    return redirect("academics:level_list")


# ---------------- Course ----------------

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
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated.")
            return redirect("academics:course_list")
    else:
        form = CourseForm(instance=course)

    return render(request, "academics/course_form.html", {"form": form, "course": course})


@login_required
@admin_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        try:
            course.delete()
            messages.success(request, "Course deleted.")
        except Exception:
            messages.error(
                request,
                "This course can't be deleted while it still has curriculum entries, "
                "allocations, or results linked to it."
            )
    return redirect("academics:course_list")


# ---------------- Curriculum ----------------

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
def curriculum_update(request, pk):
    entry = get_object_or_404(Curriculum, pk=pk)
    if request.method == "POST":
        form = CurriculumForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, "Curriculum entry updated.")
            return redirect("academics:curriculum_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CurriculumForm(instance=entry)

    return render(request, "academics/curriculum_form.html", {"form": form, "entry": entry})


@login_required
@admin_required
def curriculum_delete(request, pk):
    entry = get_object_or_404(Curriculum, pk=pk)
    if request.method == "POST":
        entry.delete()
        messages.success(request, "Curriculum entry removed.")
    return redirect("academics:curriculum_list")



@login_required
@admin_required
def session_list(request):
    if request.method == "POST":
        form = SessionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Session created — First and Second semester were added automatically.")
            return redirect("academics:session_list")
    else:
        form = SessionForm()

    sessions = Session.objects.prefetch_related("semesters").all()
    return render(request, "academics/session_list.html", {"sessions": sessions, "form": form})


@login_required
@admin_required
def session_update(request, pk):
    session = get_object_or_404(Session, pk=pk)
    if request.method == "POST":
        form = SessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, "Session updated.")
            return redirect("academics:session_list")
    else:
        form = SessionForm(instance=session)

    return render(request, "academics/session_form.html", {"form": form, "session": session})


@login_required
@admin_required
def session_delete(request, pk):
    session = get_object_or_404(Session, pk=pk)
    if request.method == "POST":
        try:
            session.delete()
            messages.success(request, "Session deleted.")
        except Exception:
            messages.error(
                request,
                "This session can't be deleted while semesters, allocations, or results still reference it."
            )
    return redirect("academics:session_list")


@login_required
@admin_required
def session_set_current(request, pk):
    if request.method == "POST":
        session = get_object_or_404(Session, pk=pk)
        session.is_current = True
        session.save()  # save() unsets every other "current" session
        messages.success(request, f"{session.name} is now the current session.")
    return redirect("academics:session_list")


@login_required
@admin_required
def semester_set_current(request, pk):
    """No full CRUD for semesters -- just a toggle for which one is active right now."""
    if request.method == "POST":
        semester = get_object_or_404(Semester, pk=pk)
        semester.is_current = True
        semester.save()
        messages.success(request, f"{semester} is now the current semester.")
    return redirect("academics:session_list")




