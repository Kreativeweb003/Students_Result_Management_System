from django import forms
from django.contrib.auth import get_user_model
from .models import Lecturer, CourseAllocation

User = get_user_model()


class LecturerRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Lecturer
        fields = ["staff_id", "department", "title"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            role=User.Role.LECTURER,
        )
        user.set_password(self.cleaned_data["password"])
        user.save()

        lecturer = super().save(commit=False)
        lecturer.user = user
        if commit:
            lecturer.save()
        return lecturer


class CourseAllocationForm(forms.ModelForm):
    class Meta:
        model = CourseAllocation
        fields = ["lecturer", "course", "session", "semester"]









