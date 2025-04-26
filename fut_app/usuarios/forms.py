from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import validate_email

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        validators=[validate_email]
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=6
    )
