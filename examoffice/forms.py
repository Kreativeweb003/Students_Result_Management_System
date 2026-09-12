from django import forms
from django.contrib.auth import get_user_model
from .models import ExamOfficer

User = get_user_model()


class ExamOfficerRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = ExamOfficer
        fields = ["staff_id", "department"]

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
            role=User.Role.EXAM_OFFICE,
        )
        user.set_password(self.cleaned_data["password"])
        user.save()

        officer = super().save(commit=False)
        officer.user = user
        if commit:
            officer.save()
        return officer




