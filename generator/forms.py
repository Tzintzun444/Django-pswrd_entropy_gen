from django.utils.translation import gettext_lazy as _
from django import forms


class CreatePasswordForm(forms.Form):

    length_password = forms.IntegerField(
        widget=forms.TextInput(attrs={'placeholder': _('Length of the password')})
    )
    use_uppercase_letters = forms.BooleanField(
        required=False
    )
    use_digits = forms.BooleanField(
        required=False
    )
    use_punctuation_characters = forms.BooleanField(
        required=False
    )
    custom_characters_allowed = forms.CharField(
        max_length=50, required=False,
        widget=forms.TextInput(attrs={'placeholder': _('These characters will appear in the password')})
    )
    characters_not_allowed = forms.CharField(
        max_length=50, required=False,
        widget=forms.TextInput(attrs={'placeholder': _('These characters won\'t appear in the password')})
    )

    def clean(self):
        cleaned_data = super().clean()
        characters_not_allowed = self.cleaned_data.get('characters_not_allowed')
        custom_characters_allowed = self.cleaned_data.get('custom_characters_allowed')
        length_password = self.cleaned_data.get('length_password')

        if not (1 <= length_password <= 30):

            self.add_error('length_password', _('Must be between 1 to 30'))

        if characters_not_allowed:
            if any([character in custom_characters_allowed for character in characters_not_allowed]):
                self.add_error(
                    'characters_not_allowed',
                    _('A character is crashing in custom and not allowed characters')
                )

        if custom_characters_allowed:
            boolean_fields = [
                self.cleaned_data.get('use_uppercase_letters'),
                self.cleaned_data.get('use_digits'),
                self.cleaned_data.get('use_punctuation_characters')
            ]

            for situation in boolean_fields:

                if situation:

                    length_password -= 1

            if length_password <= len(set(custom_characters_allowed)):

                self.add_error(
                    'custom_characters_allowed',
                    _('There are more custom characters than available characters in the length of the password.')
                )

            return cleaned_data
