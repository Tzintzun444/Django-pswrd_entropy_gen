from django import forms
from django.utils.translation import gettext_lazy as _
from .models import UserNotVerified, CustomUser
from django.contrib.auth.forms import AuthenticationForm


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

    is_admin = forms.BooleanField(
        label=_('Is admin:'),
        initial=False,
        required=False
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
            self.add_error('password', _('Password can\'t be only numeric'))

        if password1 != password2:
            self.add_error('confirm_password', "Passwords don't match")

        return cleaned_data

    def save(self, commit=True):

        is_admin = self.cleaned_data.get('is_admin', False)
        user_not_verified = UserNotVerified(
            email=self.cleaned_data['email'],
            data={
                'username': self.cleaned_data['username'],
                'first_name': self.cleaned_data['first_name'],
                'last_name': self.cleaned_data['last_name'],
                'password': self.cleaned_data['password'],
                'is_admin': is_admin
            }
        )

        if commit:
            user_not_verified.save()

        return user_not_verified

    def validate_unique(self):
        pass


class CodeInputWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [forms.TextInput(attrs={
            "maxlength": "1",
            "class": "code-input",
            "inputmode": "numeric"
        }) for _ in range(6)]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return list(value)
        return [""] * 6

    def value_from_datadict(self, data, files, name):
        values = super().value_from_datadict(data, files, name)
        cleaned_values = [v if v is not None else '' for v in values]
        return ''.join(cleaned_values)


class VerificationEmailForm(forms.Form):

    code = forms.CharField(
        label=_("Code:"),
        widget=CodeInputWidget(),
        required=True
    )

    def clean(self):

        cleaned_data = super().clean()
        code = cleaned_data.get('code', '')
        if len(code) != 6:

            self.add_error('code', _('Code must be 6 digits'))

        if not code.isdigit():

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

    email = forms.EmailField(
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
        if self.instance and self.instance.pk:
            self.initial['email'] = self.instance.email

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        new_password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if CustomUser.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            self.add_error('username', _('Username already exists'))

        if new_password:
            if len(new_password) < 8:
                self.add_error('password', _('At least 8 characters'))
            if new_password.isdigit():
                self.add_error('password', _('Password can\'t be only numeric'))
            if new_password != confirm_password:
                self.add_error('confirm_password', _('Passwords don\'t match'))

        cleaned_data['email'] = self.instance.email
        return cleaned_data
