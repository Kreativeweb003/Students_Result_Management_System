from django.db import models
from django.conf import settings
from academics.models import Department, Programme, Level, Session


class Student(models.Model):
    class StudyMode(models.TextChoices):
        FULL_TIME = "FT", "Full-Time"
        PART_TIME = "PT", "Part-Time"

    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    matric_number = models.CharField(max_length=30, unique=True, editable=False, blank=True)

    gender = models.CharField(max_length=1, choices=Gender.choices)
    date_of_birth = models.DateField(null=True, blank=True)

    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="students")
    programme = models.ForeignKey(Programme, on_delete=models.SET_NULL, null=True, related_name="students")
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, related_name="students")
    admission_session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True, related_name="admitted_students")
    study_mode = models.CharField(max_length=2, choices=StudyMode.choices, default=StudyMode.FULL_TIME)

    class Meta:
        ordering = ["matric_number"]

    def __str__(self):
        return f"{self.matric_number} - {self.user.get_full_name() or self.user.username}"

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username

    def generate_matric_number(self):
        """
        Format: DEPTCODE/PROGRAMME/MODE+YEAR/SEQUENCE
        Example: CS/ND/F24/4140
        """
        if not self.department or not self.programme or not self.admission_session:
            return None

        dept_code = self.department.code
        programme_code = self.programme.name  # ND or HND
        mode_letter = "F" if self.study_mode == self.StudyMode.FULL_TIME else "P"
        # admission_session.name is expected like "2024/2025" -> take last 2 digits of first year
        year_part = self.admission_session.name.split("/")[0][-2:]

        prefix = f"{dept_code}/{programme_code}/{mode_letter}{year_part}"

        # find the highest existing sequence number for this exact prefix
        existing = Student.objects.filter(matric_number__startswith=prefix).exclude(pk=self.pk)
        max_seq = 0
        for s in existing:
            try:
                seq = int(s.matric_number.split("/")[-1])
                max_seq = max(max_seq, seq)
            except (ValueError, IndexError):
                continue

        next_seq = max_seq + 1
        return f"{prefix}/{next_seq:04d}"

    def save(self, *args, **kwargs):
        if not self.matric_number:
            self.matric_number = self.generate_matric_number()
        super().save(*args, **kwargs)









