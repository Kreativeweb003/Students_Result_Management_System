from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction

from accounts.decorators import admin_required, exam_office_required
from results.models import Result
from students.models import Student
from .models import ExamOfficer
from .forms import ExamOfficerRegistrationForm


@login_required
@admin_required
def register_exam_officer(request):
    if request.method == "POST":
        form = ExamOfficerRegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                officer = form.save()
            messages.success(request, f"Exam officer registered for {officer.department.code}.")
            return redirect("examoffice:officer_list")
    else:
        form = ExamOfficerRegistrationForm()

    return render(request, "examoffice/register_officer.html", {"form": form})


@login_required
@admin_required
def officer_list(request):
    officers = ExamOfficer.objects.select_related("user", "department").all()
    return render(request, "examoffice/officer_list.html", {"officers": officers})


@login_required
@exam_office_required
def dashboard(request):
    officer = get_object_or_404(ExamOfficer, user=request.user)
    pending_count = Result.objects.filter(
        course__department=officer.department, status=Result.Status.PENDING
    ).count()
    students = Student.objects.filter(
        department=officer.department
    ).select_related("user", "programme", "level")

    return render(request, "examoffice/dashboard.html", {
        "officer": officer,
        "pending_count": pending_count,
        "students": students,
    })
  


@login_required
@exam_office_required
def pending_results(request):
    """Results awaiting review, scoped to the officer's own department only."""
    officer = get_object_or_404(ExamOfficer, user=request.user)
    results = Result.objects.filter(
        course__department=officer.department, status=Result.Status.PENDING
    ).select_related("student", "course", "session", "semester")

    return render(request, "examoffice/pending_results.html", {"officer": officer, "results": results})


@login_required
@exam_office_required
def approve_all_pending(request):
    officer = get_object_or_404(ExamOfficer, user=request.user)

    if request.method == "POST":
        updated = Result.objects.filter(
            course__department=officer.department,
            status=Result.Status.PENDING,
        ).update(status=Result.Status.APPROVED, reviewed_by=officer)

        messages.success(request, f"{updated} result(s) approved for {officer.department.code}.")

    return redirect("examoffice:pending_results")

@login_required
@exam_office_required
def reject_result(request, pk):
    officer = get_object_or_404(ExamOfficer, user=request.user)
    result = get_object_or_404(Result, pk=pk, course__department=officer.department)

    if request.method == "POST":
        reason = request.POST.get("reason", "").strip()
        result.status = Result.Status.REJECTED
        result.reviewed_by = officer
        result.rejection_reason = reason
        result.save()
        messages.warning(request, f"Rejected {result.student.matric_number} — {result.course.code}. The lecturer will need to re-enter it.")

    return redirect("examoffice:pending_results")




login_required
@exam_office_required
def student_results(request, pk):
    officer = get_object_or_404(ExamOfficer, user=request.user)
    # scoped: only a student in this officer's own department is reachable, even by guessing the URL
    student = get_object_or_404(Student, pk=pk, department=officer.department)

    results = Result.objects.filter(student=student).select_related(
        "course", "session", "semester"
    ).order_by("-session", "semester")

    return render(request, "examoffice/student_results.html", {
        "officer": officer,
        "student": student,
        "results": results,
    })







  



