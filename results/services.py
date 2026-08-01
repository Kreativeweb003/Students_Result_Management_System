from django.db.models import Sum, F, DecimalField, ExpressionWrapper

from .models import Result


def calculate_gpa(student, session, semester):
    """
    GPA = sum(grade_point * course_unit) / sum(course_unit)
    for a single semester.
    """
    results = Result.objects.filter(student=student, session=session, semester=semester)

    if not results.exists():
        return 0.0

    weighted = results.annotate(
        weighted_point=ExpressionWrapper(
            F("grade_point") * F("course__unit"), output_field=DecimalField()
        )
    ).aggregate(
        total_weighted=Sum("weighted_point"),
        total_units=Sum("course__unit"),
    )

    total_weighted = weighted["total_weighted"] or 0
    total_units = weighted["total_units"] or 0

    if total_units == 0:
        return 0.0

    return round(float(total_weighted) / float(total_units), 2)


def calculate_cgpa(student):
    """
    CGPA = sum(grade_point * course_unit) / sum(course_unit)
    across ALL sessions/semesters for the student.
    """
    results = Result.objects.filter(student=student)

    if not results.exists():
        return 0.0

    weighted = results.annotate(
        weighted_point=ExpressionWrapper(
            F("grade_point") * F("course__unit"), output_field=DecimalField()
        )
    ).aggregate(
        total_weighted=Sum("weighted_point"),
        total_units=Sum("course__unit"),
    )

    total_weighted = weighted["total_weighted"] or 0
    total_units = weighted["total_units"] or 0

    if total_units == 0:
        return 0.0

    return round(float(total_weighted) / float(total_units), 2)


def get_academic_standing(cgpa):
    """Simple standing lookup -- adjust bands to match your school's policy."""
    if cgpa >= 4.5:
        return "First Class / Distinction"
    elif cgpa >= 3.5:
        return "Second Class Upper / Upper Credit"
    elif cgpa >= 2.4:
        return "Second Class Lower / Lower Credit"
    elif cgpa >= 1.5:
        return "Third Class / Pass"
    else:
        return "Probation"