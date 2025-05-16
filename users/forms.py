from django import forms
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm


class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:

        model = CustomUser
        fields = ['username', 'email', 'password',]

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
