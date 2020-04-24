import re

from django import forms
from django.conf import settings

from core.models import BaseUserProfile
from core.backends import EmailModelBackend


class LoginForm(forms.Form):
    """
    Login form view for validating user login. Throw validation
    as handled below
    """

    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()

        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not (email or password):
            msg = "Email and password are required"
            self._errors["password"] = self.error_class(["Password is required"])
            self._errors["email"] = self.error_class(["Email is required."])
            return self.cleaned_data

        if not password:
            msg = "Password is required"
            self._errors["password"] = self.error_class([msg])
            return self.cleaned_data

        if not email:
            msg = "Email is required"
            self._errors["email"] = self.error_class([msg])
            return self.cleaned_data

        user_auth = EmailModelBackend()
        user = user_auth.authenticate(username=email, password=password)

        if user is None:
            msg = "Email or password is incorrect"
            self._errors["password"] = self.error_class([msg])
            return self.cleaned_data

        if not user.is_active:
            msg = "Your account is not activated"
            self._errors["password"] = self.error_class([msg])
            return self.cleaned_data

        return self.cleaned_data


class SignUpForm(forms.ModelForm):
    """
    SignUpForm for user sign up, it will handle validation as given below
    """

    password = forms.CharField(
        widget=forms.PasswordInput(),
        label="password",
        max_length=50,
        error_messages={"required": "Please enter your password."},
    )
    email = forms.CharField(
        label="email", error_messages={"required": "Please enter your email."}
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        label="confirm_password",
        max_length=50,
        error_messages={"required": "Please enter confirm password."},
    )

    class Meta:
        model = BaseUserProfile
        fields = ("password", "email")

    def save(self):
        base_user = super(SignUpForm, self).save(commit=False)
        base_user.set_password(self.cleaned_data["password"])
        base_user.username = self.cleaned_data["email"]
        base_user.email = self.cleaned_data["email"]
        base_user.is_active = True
        base_user.save()
        print(base_user)
        return self.cleaned_data

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        email = cleaned_data.get("email")
        confirm_password = cleaned_data.get("confirm_password")
        password = cleaned_data.get("password")
        user = BaseUserProfile.objects.filter(email__iexact=email)

        if user:
            msg = "User with the same email already exists!"
            self._errors["email"] = self.error_class([msg])
            return self.cleaned_data

        if not email:
            msg = "Email address required"
            self._errors["email"] = self.error_class([msg])
            return self.cleaned_data

        if password != confirm_password:
            msg = "Both passwords do not match"
            self._errors["password"] = self.error_class([msg])


class ProfileForm(forms.Form):
    """
    This form is used to handle profile submission
    """

    email = forms.CharField()
    phone_no = forms.CharField()
    message = forms.CharField()
    full_name = forms.CharField()

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        email = cleaned_data.get("email")
        message = cleaned_data.get("message")
        full_name = cleaned_data.get("full_name")
        phone_no = cleaned_data.get("phone_no")

        if not (email):
            self._errors["email"] = self.error_class(["Email is required."])

        if not message:
            self._errors["message"] = self.error_class(["Message is required"])

        if not full_name:
            self._errors["full_name"] = self.error_class(["Full name is required"])

        if not phone_no:
            self._errors["phone_no"] = self.error_class(["Phone no is required"])

        if phone_no and not re.match(r"^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$", phone_no):
            self._errors["phone_no"] = self.error_class(["Please enter valid phone no eg. +91-9292923233 or 9292923233"])
        return self.cleaned_data
