from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()


class SignUpForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    def save(self):
        return User.objects.create_user(**self.cleaned_data)
