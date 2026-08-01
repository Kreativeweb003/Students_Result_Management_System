from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction

from accounts.decorators import admin_required, student_required
from .models import Student
from .forms import StudentRegistrationForm, StudentProfileUpdateForm


@login_required
@admin_required
def register_student(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                student = form.save()
            messages.success(request, f"Student registered. Matric No: {student.matric_number}")
            return redirect("students:student_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StudentRegistrationForm()

    return render(request, "students/register_student.html", {"form": form})


@login_required
@admin_required
def student_list(request):
    students = Student.objects.select_related("user", "department", "programme", "level").all()

    # simple filters, useful once you have a few hundred records
    department_id = request.GET.get("department")
    level_id = request.GET.get("level")
    if department_id:
        students = students.filter(department_id=department_id)
    if level_id:
        students = students.filter(level_id=level_id)

    return render(request, "students/student_list.html", {"students": students})


@login_required
@admin_required
def student_detail(request, pk):
    student = get_object_or_404(Student.objects.select_related("user", "department", "programme", "level"), pk=pk)
    return render(request, "students/student_detail.html", {"student": student})


@login_required
@student_required
def student_dashboard(request):
    student = get_object_or_404(Student, user=request.user)
    return render(request, "students/dashboard.html", {"student": student})


@login_required
@student_required
def student_profile(request):
    student = get_object_or_404(Student, user=request.user)
    if request.method == "POST":
        form = StudentProfileUpdateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("students:profile")
    else:
        form = StudentProfileUpdateForm(instance=student)

    return render(request, "students/profile.html", {"form": form, "student": student})