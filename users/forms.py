import re
from django import forms
from django.contrib.auth.models import User, Permission, Group
from tasks.forms import StyledFormMixin
from django.contrib.auth.forms import AuthenticationForm

class CustomRegistrationForm(StyledFormMixin,forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'confirm_password', 'email']


    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=email)

        # Check if the email is already registered
        if email_exists:
            raise forms.ValidationError("This email is already in use. Please choose a different one.")

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long')

        # Ensure password contains at least one uppercase, lowercase, digit, and special character
        if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'\d', password) or not re.search(r'[@#$%^&+=]', password):
            raise forms.ValidationError("Password must include an uppercase letter, a lowercase letter, a number, and a special character")

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data
    
class LoginForm(StyledFormMixin,AuthenticationForm):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)

    
class AssignRoleForm(StyledFormMixin,forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label = "Select a Role"
    )

class CreateGroupForm(StyledFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required = False,
        label = 'Assign Permission'
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']





