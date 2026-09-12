from django.db import models
from django.conf import settings
from academics.models import Department


class ExamOfficer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="exam_officer_profile")
    staff_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="exam_officers")

    class Meta:
        ordering = ["department", "user__last_name"]

    def __str__(self):
        return f"{self.full_name} — {self.department.code} Exam Office"

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username