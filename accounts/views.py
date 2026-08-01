from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import LoginForm, PasswordChangeCustomForm


class RoleBasedLoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm

    def get_success_url(self):
        user = self.request.user
        if user.is_admin:
            return reverse("academics:home")
        elif user.is_lecturer:
            return reverse("lecturers:dashboard")
        elif user.is_student:
            return reverse("students:dashboard")
        return "/"


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("accounts:login")


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeCustomForm(request.POST)
        if form.is_valid():
            user = request.user
            if not user.check_password(form.cleaned_data["old_password"]):
                messages.error(request, "Old password is incorrect.")
            else:
                user.set_password(form.cleaned_data["new_password"])
                user.save()
                update_session_auth_hash(request, user)  # keeps user logged in
                messages.success(request, "Password updated successfully.")
                return redirect("accounts:change_password")
    else:
        form = PasswordChangeCustomForm()

    return render(request, "accounts/change_password.html", {"form": form})
  



