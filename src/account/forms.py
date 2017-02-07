from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.validators import RegexValidator

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

User = get_user_model()
username_regex = '^[a-zA-Z0-9.@+-]*$'


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username', validators=[RegexValidator(
        regex=username_regex,
        message='Username must be Alphanumeric or contain any of the following: ". @ + -" ',
        code='invalid_username'
    )])
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        the_user = authenticate(username=username, password=password)
        if not the_user:
            # TODO log auth tries
            raise forms.ValidationError("Invalid Credentials")

        return super(UserLoginForm, self).clean()

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Login', css_class='btn=primary'))
