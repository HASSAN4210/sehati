from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class ArabicAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="اسم المستخدم",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "username",
                "autofocus": True,
                "placeholder": "أدخل اسم المستخدم",
            }
        ),
    )
    password = forms.CharField(
        label="كلمة المرور",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": "أدخل كلمة المرور",
            }
        ),
    )


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label="اسم المستخدم",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "username",
                "autofocus": True,
                "placeholder": "اختر اسم مستخدم",
            }
        ),
    )
    password1 = forms.CharField(
        label="كلمة المرور",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "أنشئ كلمة مرور قوية",
            }
        ),
    )
    password2 = forms.CharField(
        label="تأكيد كلمة المرور",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "أعد كتابة كلمة المرور",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
