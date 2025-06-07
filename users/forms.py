from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from .models import UserNotVerified, CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate


class UserRegistrationForm(forms.ModelForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": _("Letters, digits and @.+-_ only"),
                   "autocomplete": "off"
                   }),
        max_length=150,
        label=_('Username:')
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": _("First name"),
                   "autocomplete": "off"
                   }),
        max_length=50,
        label=_('First name:')
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": _("Last name"),
                   "autocomplete": "off"
                   }),
        max_length=50,
        label=_('Last name:')
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": _("Enter an email address"),
                   "autocomplete": "off"
                   }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": _("At least 8 characters"),
                   "autocomplete": "off"
                   }),
        min_length=8,
        label=_('Password:')
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": _("Repeat your password"),
                   "autocomplete": "off"
                   }),
        label=_('Confirm password:')
    )

    class Meta:

        model = UserNotVerified
        fields = ['email']

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get('email')
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("confirm_password")

        if CustomUser.objects.filter(username=username).exists():

            self.add_error('username', _('Username already exists'))

        if CustomUser.objects.filter(email=email).exists():

            self.add_error('email', _('Email already in use'))

        if password1.isnumeric():
            self.add_error('password', _('Paswword can\'t be only numeric'))

        if password1 != password2:
            self.add_error('confirm_password', "Passwords don't match")

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)
        user.data = {
            'username': self.cleaned_data['username'],
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name'],
            'password': self.cleaned_data['password']
        }

        if commit:
            user.save()

        return user


class VerificationEmailForm(forms.Form):

    code = forms.CharField(
        max_length=6,
        label=_('Code:'),
        validators=[MinLengthValidator(6)],
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )

    def clean(self):

        cleaned_data = super().clean()
        code = self.cleaned_data['code']

        if not code.isnumeric():

            self.add_error('code', _('Only numbers are allowed'))

        return cleaned_data


class CustomLoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "login-input", "placeholder": _("Username")}),
        label=_('Username:')
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "login-input", "placeholder": _("Password")}),
        label=_('Password:')
    )

    error_messages = {
        "invalid_login": _(
            "Invalid data, please try again"
        ),
        "inactive": _("This account is inactive"),
    }


class UserSettingsForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': _('At least 8 characters')}),
        label=_('New password:'),
        required=False,
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': _('Repeat your password')}),
        label=_('Confirm password:'),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
            'username': forms.TextInput(attrs={'placeholder': _("Letters, digits and @.+-_ only")}),
            'first_name': forms.TextInput(attrs={'placeholder': _('First name')}),
            'last_name': forms.TextInput(attrs={'placeholder': _('Last name')}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mantener el email original siempre
        if self.instance and self.instance.pk:
            self.initial['email'] = self.instance.email

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        new_password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if CustomUser.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            self.add_error('username',_('Username already exists'))

        if new_password:
            if len(new_password) < 8:
                self.add_error('password', _('At least 8 characters'))
            if new_password.isnumeric():
                self.add_error('password', _('Password cannot be only numeric'))
            if new_password != confirm_password:
                self.add_error('confirm_password', _('Passwords do not match'))
        return cleaned_data
