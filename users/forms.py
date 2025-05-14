from django import forms
from .models import CustomUser


class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:

        model = CustomUser
        fields = ['username', 'email', 'password', 'role',]

    def save(self, commit=True):

        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
