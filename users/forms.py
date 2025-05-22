from django import forms
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

user = get_user_model()


class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "login-input", "placeholder": "Password"}),
        help_text='At least 8 characters', min_length=8
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "login-input", "placeholder": "Repeat your password"})
    )

    class Meta:

        model = CustomUser
        fields = ['username', 'email', 'password',]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("confirm_password")

        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user


class CustomLoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "login-input", "placeholder": "Username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "login-input", "placeholder": "Password"})
    )
