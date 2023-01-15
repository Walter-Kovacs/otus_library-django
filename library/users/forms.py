from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.models import Librarian


class RegistrationForm(UserCreationForm):
    username = forms.CharField()
    first_name = forms.CharField(
        required=True,
    )
    last_name = forms.CharField(
        required=True,
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput,
    )
    phone = forms.CharField(
        max_length=32,
    )
    address = forms.CharField(
        widget=forms.Textarea,
    )

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )


class ReaderRegistrationForm(RegistrationForm):
    pass


class LibrarianRegistrationForm(RegistrationForm):
    pass


class RegisterLibrarianForm(forms.ModelForm):
    staff_number = forms.CharField(
        min_length=1,
        max_length=8,
    )

    class Meta:
        model = Librarian
        fields = ('staff_number', )
