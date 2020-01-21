from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    """Form definition for UserAdminCreation."""
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="password confirmation", widget=forms.PasswordInput)

    class Meta:
        """Meta definition for UserAdminCreationform."""

        model = User
        fields = ('email',)

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("passwords must be same")
        return password1

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get("password1"))
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """Form definition for UserAdminChange."""

    password = ReadOnlyPasswordHashField()

    class Meta:
        """Meta definition for UserAdminChangeform."""

        model = User
        fields = ('email', 'password', 'active', 'admin')

    def clean_password(self):
        return self.initial["password"]


class GuestForm(forms.Form):
    email = forms.EmailField()


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(forms.ModelForm):
    """Form definition for UserAdminCreation."""
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="password confirmation", widget=forms.PasswordInput)

    class Meta:
        """Meta definition for UserAdminCreationform."""

        model = User
        fields = ('email',)

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("passwords must be same")
        return password1

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get("password1"))
        user.active = True
        if commit:
            user.save()
        return user
