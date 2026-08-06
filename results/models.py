from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from students.models import Student
from academics.models import Course, Session, Semester
from lecturers.models import Lecturer


class GradingScale(models.Model):
    """
    Configurable score -> grade -> grade point mapping.
    Kept as a model (not hardcoded) so it can be adjusted without touching code.
    """
    min_score = models.PositiveSmallIntegerField()
    max_score = models.PositiveSmallIntegerField()
    grade = models.CharField(max_length=2)  # A, B, C, D, F
    grade_point = models.DecimalField(max_digits=3, decimal_places=1)  # e.g. 5.0, 4.0

    class Meta:
        ordering = ["-min_score"]

    def __str__(self):
        return f"{self.min_score}-{self.max_score} = {self.grade} ({self.grade_point})"

    def clean(self):
        if self.min_score > self.max_score:
            raise ValidationError("min_score cannot be greater than max_score.")

    @classmethod
    def get_grade_for_score(cls, score):
        band = cls.objects.filter(min_score__lte=score, max_score__gte=score).first()
        if not band:
            return None, None
        return band.grade, band.grade_point


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="results")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="results")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="results")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="results")
    lecturer = models.ForeignKey(Lecturer, on_delete=models.SET_NULL, null=True, related_name="entered_results")

    ca_score = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(30)])
    exam_score = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(70)])

    total_score = models.DecimalField(max_digits=5, decimal_places=2, editable=False, default=0)
    grade = models.CharField(max_length=2, editable=False, blank=True)
    grade_point = models.DecimalField(max_digits=3, decimal_places=1, editable=False, default=0)

    is_published = models.BooleanField(default=False)  # admin controls student visibility
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "course", "session", "semester")
        ordering = ["-session", "semester", "student"]

    def __str__(self):
        return f"{self.student.matric_number} - {self.course.code}: {self.total_score} ({self.grade})"

    def clean(self):
        if self.ca_score + self.exam_score > 100:
            raise ValidationError("CA score + Exam score cannot exceed 100.")

    def compute_grade(self):
        self.total_score = self.ca_score + self.exam_score
        grade, grade_point = GradingScale.get_grade_for_score(self.total_score)
        self.grade = grade or ""
        self.grade_point = grade_point or 0

    def save(self, *args, **kwargs):
        self.compute_grade()
        super().save(*args, **kwargs)








