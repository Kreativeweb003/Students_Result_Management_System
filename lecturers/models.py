from django.db import models
from django.conf import settings
from academics.models import Course, Department, Session, Semester


class Lecturer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lecturer_profile")
    staff_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="lecturers")
    title = models.CharField(max_length=20, blank=True)  # e.g. "Mr.", "Dr.", "Mrs."

    class Meta:
        ordering = ["user__last_name", "user__first_name"]

    def __str__(self):
        return f"{self.title} {self.user.get_full_name() or self.user.username}".strip()

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username


class CourseAllocation(models.Model):
    """
    Assigns a lecturer to a course for a specific session/semester.
    A lecturer can only enter scores for courses allocated to them here.
    """
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name="allocations")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="allocations")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="course_allocations")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="course_allocations")

    class Meta:
        unique_together = ("course", "session", "semester")
        # one lecturer per course per session/semester -- change to allow co-teaching if needed
        ordering = ["-session", "semester", "course"]

    def __str__(self):
        return f"{self.lecturer.full_name} -> {self.course.code} ({self.session}, {self.semester.get_name_display()})"




