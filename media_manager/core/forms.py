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
            msg = "Email and password is required"
            self._errors["password"] = self.error_class([msg])
            del self._errors["email"]
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

    usertype = forms.CharField(label="usertype")
    firstname = forms.CharField(
        label="firstname",
        max_length=25,
        error_messages={"required": "Please enter your first name."},
    )
    lastname = forms.CharField(
        label="lastname",
        max_length=25,
        error_messages={"required": "Please enter your last name."},
    )
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
        fields = ("first_name", "last_name", "password", "email")

    def save(self):
        email = self.cleaned_data["email"]
        base_user = super(SignUpForm, self).save(commit=False)
        base_user.set_password(self.cleaned_data["password"])
        first_name = self.cleaned_data["firstname"]
        last_name = self.cleaned_data["lastname"]
        usertype = self.cleaned_data["usertype"]
        base_user.first_name = first_name
        base_user.last_name = last_name
        base_user.username = first_name
        base_user.user_type = usertype
        base_user.is_active = False
        base_user.save()
        return self.cleaned_data

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        email = cleaned_data.get("email")
        confirm_password = cleaned_data.get("confirm_password")
        password = cleaned_data.get("password")
        user = BaseUserProfile.objects.filter(email__iexact=email)
        if not email:
            msg = "Email address required"
            self._errors["email"] = self.error_class([msg])
            return self.cleaned_data

        if password != confirm_password:
            msg = "Both passwords do not match"
            self._errors["password"] = self.error_class([msg])

