from django import forms
from django.contrib.auth import get_user_model
from .models import Student

User = get_user_model()


class StudentRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = [
            "gender", "date_of_birth", "department", "programme",
            "level", "admission_session", "study_mode",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }

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

    def clean(self):
        cleaned_data = super().clean()
        programme = cleaned_data.get("programme")
        level = cleaned_data.get("level")
        if programme and level and level.programme_id != programme.id:
            raise forms.ValidationError("Selected level does not belong to the selected programme.")
        return cleaned_data

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            role=User.Role.STUDENT,
        )
        user.set_password(self.cleaned_data["password"])
        user.save()

        student = super().save(commit=False)
        student.user = user
        if commit:
            student.save()  # matric_number auto-generated here
        return student


class StudentProfileUpdateForm(forms.ModelForm):
    """Limited self-service update -- students should not touch academic fields."""
    class Meta:
        model = Student
        fields = ["date_of_birth"]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }