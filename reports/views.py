from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from accounts.decorators import student_required, admin_required
from students.models import Student
from academics.models import Session, Semester
from results.models import Result
from .generators import generate_result_slip_pdf, generate_transcript_pdf


@login_required
@student_required
def download_result_slip(request, session_id, semester_id):
    student = get_object_or_404(Student, user=request.user)
    session = get_object_or_404(Session, pk=session_id)
    semester = get_object_or_404(Semester, pk=semester_id)

    results = Result.objects.filter(
        student=student, session=session, semester=semester, is_published=True
    ).select_related("course")

    if not results.exists():
        return HttpResponse("No published results found for this semester.", status=404)

    buffer = generate_result_slip_pdf(student, session, semester, results)
    response = HttpResponse(buffer, content_type="application/pdf")
    filename = f"{student.matric_number}_{session.name}_{semester.name}_slip.pdf".replace("/", "-")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


@login_required
@student_required
def download_transcript(request):
    student = get_object_or_404(Student, user=request.user)

    published_results = Result.objects.filter(
        student=student, is_published=True
    ).select_related("course", "session", "semester").order_by("session", "semester")

    # group results by (session, semester)
    grouped = {}
    for r in published_results:
        key = (r.session_id, r.semester_id)
        if key not in grouped:
            grouped[key] = {"session": r.session, "semester": r.semester, "results": []}
        grouped[key]["results"].append(r)

    if not grouped:
        return HttpResponse("No published results found.", status=404)

    buffer = generate_transcript_pdf(student, list(grouped.values()))
    response = HttpResponse(buffer, content_type="application/pdf")
    filename = f"{student.matric_number}_transcript.pdf".replace("/", "-")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


@login_required
@admin_required
def department_statistics(request):
    """
    Simple pass/fail and average score breakdown per course,
    filterable by session/semester via query params.
    """
    from django.db.models import Avg, Count, Q

    session_id = request.GET.get("session")
    semester_id = request.GET.get("semester")

    results = Result.objects.all()
    if session_id:
        results = results.filter(session_id=session_id)
    if semester_id:
        results = results.filter(semester_id=semester_id)

    course_stats = results.values("course__code", "course__title").annotate(
        average_score=Avg("total_score"),
        total_students=Count("id"),
        pass_count=Count("id", filter=Q(total_score__gte=40)),  # adjust pass mark to your policy
        fail_count=Count("id", filter=Q(total_score__lt=40)),
    ).order_by("course__code")

    return render(request, "reports/department_statistics.html", {
        "course_stats": course_stats,
        "sessions": Session.objects.all(),
        "semesters": Semester.objects.all(),
    })







