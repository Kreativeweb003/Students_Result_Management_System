from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrator"
        EXAM_OFFICE = "EXAM_OFFICE", "Exam Office"
        LECTURER = "LECTURER", "Lecturer"
        STUDENT = "STUDENT", "Student"

    role = models.CharField(max_length=12, choices=Role.choices, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_exam_office(self):
        return self.role == self.Role.EXAM_OFFICE

    @property
    def is_lecturer(self):
        return self.role == self.Role.LECTURER

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"


