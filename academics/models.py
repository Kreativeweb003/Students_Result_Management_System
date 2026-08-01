from django.db import models
from django.core.exceptions import ValidationError


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)  # e.g. CS

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Programme(models.Model):
    class ProgrammeType(models.TextChoices):
        ND = "ND", "National Diploma"
        HND = "HND", "Higher National Diploma"

    name = models.CharField(max_length=10, choices=ProgrammeType.choices, unique=True)

    def __str__(self):
        return self.get_name_display()


class Level(models.Model):
    # e.g. ND I, ND II, HND I, HND II
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name="levels")
    name = models.CharField(max_length=20)  # e.g. "I", "II"

    class Meta:
        unique_together = ("programme", "name")
        ordering = ["programme", "name"]

    def __str__(self):
        return f"{self.programme.name} {self.name}"


class Session(models.Model):
    # e.g. "2024/2025"
    name = models.CharField(max_length=20, unique=True)
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # ensure only one session is marked current
        if self.is_current:
            Session.objects.exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)


class Semester(models.Model):
    class SemesterName(models.TextChoices):
        FIRST = "FIRST", "First Semester"
        SECOND = "SECOND", "Second Semester"

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="semesters")
    name = models.CharField(max_length=10, choices=SemesterName.choices)
    is_current = models.BooleanField(default=False)

    class Meta:
        unique_together = ("session", "name")
        ordering = ["session", "name"]

    def __str__(self):
        return f"{self.get_name_display()} - {self.session.name}"

    def save(self, *args, **kwargs):
        if self.is_current:
            Semester.objects.exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)


class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)  # e.g. CSC111
    title = models.CharField(max_length=200)
    unit = models.PositiveSmallIntegerField(default=2)  # credit unit, used in GPA calc
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses")

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.title}"


class Curriculum(models.Model):
    """
    Maps a course to a specific department/programme/level/semester.
    This determines which students are eligible for which courses,
    replacing student self-registration.
    """
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    semester_name = models.CharField(max_length=10, choices=Semester.SemesterName.choices)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="curriculum_entries")

    class Meta:
        unique_together = ("department", "programme", "level", "semester_name", "course")
        verbose_name_plural = "Curriculum"

    def clean(self):
        # guard against assigning a level that doesn't belong to the chosen programme
        if self.level.programme_id != self.programme_id:
            raise ValidationError("Selected level does not belong to the selected programme.")

    def __str__(self):
        return f"{self.course.code} - {self.department.code} {self.programme.name}{self.level.name} ({self.semester_name})"







