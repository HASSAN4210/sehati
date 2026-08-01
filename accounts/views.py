from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render

from .forms import ArabicAuthenticationForm, RegistrationForm


class UserLoginView(LoginView):
    authentication_form = ArabicAuthenticationForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = "accounts:login"


def register(request):
    if request.user.is_authenticated:
        return redirect("catalog:home")

    form = RegistrationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "تم إنشاء حسابك بنجاح، أهلًا بك في صحتي.")
        return redirect("catalog:home")

    return render(request, "accounts/register.html", {"form": form})
