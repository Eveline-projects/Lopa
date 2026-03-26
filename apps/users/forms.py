from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from apps.users.models import User


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Repeat Password'

        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = 'Your password must be at least 8 characters long.'
        self.fields['password2'].help_text = ''

class ArchitectLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Identifier_Username",
        widget=forms.TextInput(attrs={
            'placeholder': 'neo_architect',
        })
    )
    password = forms.CharField(
        label="Access_Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••••••'
        })
    )