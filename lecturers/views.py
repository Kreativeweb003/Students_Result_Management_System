from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.decorators import admin_required, lecturer_required
from academics.models import Semester
from .models import Lecturer, CourseAllocation
from .forms import LecturerRegistrationForm, CourseAllocationForm


@login_required
@admin_required
def register_lecturer(request):
    if request.method == "POST":
        form = LecturerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Lecturer registered successfully.")
            return redirect("lecturers:lecturer_list")
    else:
        form = LecturerRegistrationForm()

    return render(request, "lecturers/register_lecturer.html", {"form": form})


@login_required
@admin_required
def lecturer_list(request):
    lecturers = Lecturer.objects.select_related("user", "department").all()
    return render(request, "lecturers/lecturer_list.html", {"lecturers": lecturers})


@login_required
@admin_required
def allocate_course(request):
    if request.method == "POST":
        form = CourseAllocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Course allocated successfully.")
            return redirect("lecturers:allocation_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CourseAllocationForm()

    return render(request, "lecturers/allocate_course.html", {"form": form})


@login_required
@admin_required
def allocation_list(request):
    allocations = CourseAllocation.objects.select_related(
        "lecturer__user", "course", "session", "semester"
    ).all()
    return render(request, "lecturers/allocation_list.html", {"allocations": allocations})


@login_required
@admin_required
def allocation_delete(request, pk):
    allocation = get_object_or_404(CourseAllocation, pk=pk)
    allocation.delete()
    messages.success(request, "Allocation removed.")
    return redirect("lecturers:allocation_list")


@login_required
@lecturer_required
def lecturer_dashboard(request):
    lecturer = get_object_or_404(Lecturer, user=request.user)
    current_semester = Semester.objects.filter(is_current=True).first()

    allocations = lecturer.allocations.select_related("course", "session", "semester")
    if current_semester:
        allocations = allocations.filter(semester=current_semester)

    return render(request, "lecturers/dashboard.html", {
        "lecturer": lecturer,
        "allocations": allocations,
        "current_semester": current_semester,
    })





