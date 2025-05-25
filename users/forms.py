from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from .models import UserNotVerified, CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password

user = get_user_model()


class UserRegistrationForm(forms.ModelForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Letters, digits and @/./+/-/_ only.",
                   "autocomplete": "off"
                   }),
        max_length=150
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "First name",
                   "autocomplete": "off"
                   }),
        max_length=50
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Last name",
                   "autocomplete": "off"
                   }),
        max_length=50
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "Enter an email address",
                   "autocomplete": "off"
                   })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "At least 8 characters",
                   "autocomplete": "off"
                   }),
        min_length=8
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Repeat your password",
                   "autocomplete": "off"
                   })
    )

    class Meta:

        model = UserNotVerified
        fields = ['email']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("confirm_password")

        if password1 != password2:
            self.add_error('confirm_password',"Passwords don't match")

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)
        user.data = {
            'username': self.cleaned_data['username'],
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name'],
            'password': make_password(self.cleaned_data['password'])
        }

        if commit:
            user.save()

        return user


class VerificationEmailForm(forms.Form):

    code = forms.CharField(
        max_length=6,
        validators=[MinLengthValidator(6)],
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )


class CustomLoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "login-input", "placeholder": "Username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "login-input", "placeholder": "Password"})
    )


class UserSettingsForm(forms.ModelForm):

    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'At least 8 characters'}
        ),
        required=False,
        min_length=8
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Repeat your password'}
        ),
        required=False
    )

    class Meta:

        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'readonly': 'readonly',
            }),
            'username': forms.TextInput(
                attrs={'placeholder': 'Username'}
            ),
            'first_name': forms.TextInput(
                attrs={'placeholder': 'First name'}
            ),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Last name'}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        new_password = self.cleaned_data['new_password']
        confirm_password = self.cleaned_data['confirm_password']

        if new_password != confirm_password:
            self.add_error('confirm_password', 'Passwords don\'t match')

        return cleaned_data
