from django import forms


class CreatePasswordForm(forms.Form):

    length_password = forms.IntegerField(min_value=1, max_value=30)
    use_uppercase_letters = forms.BooleanField(required=False)
    use_digits = forms.BooleanField(required=False)
    use_punctuation_characters = forms.BooleanField(required=False)
    customized = forms.CharField(max_length=50, required=False)
    not_allowed = forms.CharField(max_length=50, required=False)
