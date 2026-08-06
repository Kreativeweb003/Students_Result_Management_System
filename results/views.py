from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal, InvalidOperation
from accounts.decorators import lecturer_required, student_required, admin_required
from lecturers.models import Lecturer, CourseAllocation
from students.models import Student
from academics.models import Semester, Session
from .models import Result
from .forms import ResultEntryForm
from .services import calculate_gpa, calculate_cgpa, get_academic_standing
from django.db.models import Q
from academics.models import Curriculum


@login_required
@lecturer_required
def select_course_for_entry(request):
    lecturer = get_object_or_404(Lecturer, user=request.user)
    current_semester = Semester.objects.filter(is_current=True).first()

    allocations = lecturer.allocations.select_related("course", "session", "semester")
    if current_semester:
        allocations = allocations.filter(semester=current_semester)

    return render(request, "results/select_course.html", {"allocations": allocations})



@login_required
@lecturer_required
def enter_results(request, allocation_id):
    lecturer = get_object_or_404(Lecturer, user=request.user)
    allocation = get_object_or_404(CourseAllocation, pk=allocation_id, lecturer=lecturer)

    curriculum_entries = Curriculum.objects.filter(
        course=allocation.course,
        semester_name=allocation.semester.name,
    ).select_related("department", "programme", "level")

    if not curriculum_entries.exists():
        messages.warning(
            request,
            "This course has no curriculum entry for the current semester. "
            "No students are eligible until an admin assigns it."
        )
        eligible_students = Student.objects.none()
    else:
        student_filter = Q()
        for entry in curriculum_entries:
            student_filter |= Q(
                department=entry.department,
                programme=entry.programme,
                level=entry.level,
            )
        eligible_students = Student.objects.filter(student_filter).select_related("user")

    if request.method == "POST":
        saved_count = 0
        skipped_count = 0

        for student in eligible_students:
            ca = request.POST.get(f"ca_{student.id}")
            exam = request.POST.get(f"exam_{student.id}")

            if ca in (None, "") or exam in (None, ""):
                continue  # lecturer hasn't scored this student yet -- fine, skip silently

            # first line of defense: catch malformed input before it's even a Decimal
            try:
                ca_value = Decimal(ca)
                exam_value = Decimal(exam)
            except InvalidOperation:
                messages.error(request, f"Invalid score entered for {student.matric_number} — skipped.")
                skipped_count += 1
                continue

            if ca_value < 0 or ca_value > 30 or exam_value < 0 or exam_value > 70:
                messages.error(
                    request,
                    f"Score out of range for {student.matric_number} "
                    f"(CA max 30, Exam max 70) — skipped."
                )
                skipped_count += 1
                continue

            # second line of defense: the model's own full_clean() runs inside save(),
            # so anything that slips past the checks above still can't reach the database
            try:
                Result.objects.update_or_create(
                    student=student,
                    course=allocation.course,
                    session=allocation.session,
                    semester=allocation.semester,
                    defaults={
                        "lecturer": lecturer,
                        "ca_score": ca_value,
                        "exam_score": exam_value,
                    },
                )
                saved_count += 1
            except DjangoValidationError as e:
                messages.error(request, f"Could not save result for {student.matric_number}: {e}")
                skipped_count += 1

        if saved_count:
            messages.success(request, f"{saved_count} result(s) saved successfully.")
        if not saved_count and not skipped_count:
            messages.info(request, "No scores were entered.")

        return redirect("results:select_course")

    existing_results = {
        r.student_id: r for r in Result.objects.filter(
            course=allocation.course, session=allocation.session, semester=allocation.semester
        )
    }

    return render(request, "results/enter_results.html", {
        "allocation": allocation,
        "students": eligible_students,
        "existing_results": existing_results,
        "curriculum_entries": curriculum_entries,
    })



@login_required
@student_required
def view_results(request):
    student = get_object_or_404(Student, user=request.user)
    results = Result.objects.filter(student=student, is_published=True).select_related(
        "course", "session", "semester"
    )

    current_semester = Semester.objects.filter(is_current=True).first()
    semester_gpa = None
    if current_semester:
        semester_gpa = calculate_gpa(student, current_semester.session, current_semester)

    cgpa = calculate_cgpa(student)
    standing = get_academic_standing(cgpa)

    return render(request, "results/view_results.html", {
        "results": results,
        "semester_gpa": semester_gpa,
        "cgpa": cgpa,
        "standing": standing,
    })


@login_required
@admin_required
def admin_result_list(request):
    results = Result.objects.select_related("student", "course", "session", "semester").all()

    session_id = request.GET.get("session")
    semester_id = request.GET.get("semester")
    if session_id:
        results = results.filter(session_id=session_id)
    if semester_id:
        results = results.filter(semester_id=semester_id)

    return render(request, "results/admin_result_list.html", {"results": results})


@login_required
@admin_required
def publish_results(request):
    """Bulk publish for a given session/semester -- simple toggle, no approval chain."""
    if request.method == "POST":
        session_id = request.POST.get("session")
        semester_id = request.POST.get("semester")
        updated = Result.objects.filter(session_id=session_id, semester_id=semester_id).update(is_published=True)
        messages.success(request, f"{updated} result(s) published for students to view.")
        return redirect("results:admin_result_list")

    return render(request, "results/publish_results.html", {
        "sessions": Session.objects.all(),
        "semesters": Semester.objects.all(),
    })




