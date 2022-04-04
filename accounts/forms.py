from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginFormView(forms.Form):
    username = forms.CharField(widget=forms.TextInput(), label='Login')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')


class RegisterFormView(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password_1 = forms.CharField(widget=forms.PasswordInput(), label='Password')
    password_2 = forms.CharField(widget=forms.PasswordInput(), label='Repeat password')
    email = forms.EmailField(label='E-mail address')

    def clean(self):
        data = super().clean()
        if data['password_1'] != data['password_2']:
            raise ValidationError("Passwords doesn't match!")

    class Meta:
        model = User
        fields = ['username', 'password_1', 'password_2', 'email']
