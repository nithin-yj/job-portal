from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm


User = get_user_model()


class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    password_confirm = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'role',
        ]

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name'].strip()

        if not first_name:
            raise forms.ValidationError("First name is required.")

        if len(first_name) > 50:
            raise forms.ValidationError(
                "First name cannot exceed 50 characters."
            )

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name'].strip()

        if not last_name:
            raise forms.ValidationError("Last name is required.")

        if len(last_name) > 50:
            raise forms.ValidationError(
                "Last name cannot exceed 50 characters."
            )

        return last_name

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def clean_password(self):
        password = self.cleaned_data['password']

        validate_password(password, self.instance)

        return password

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError(
                    "Passwords do not match."
                )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user


class LoginForm(AuthenticationForm):

    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter your email'
            }
        )
    )