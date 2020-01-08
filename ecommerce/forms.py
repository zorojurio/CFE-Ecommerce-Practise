from django import forms
from django.contrib.auth import get_user_model


class ContactForm(forms.Form):
    fullname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "full_form_name",
                "placeholder": "Enter Your Name Here",

            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Your Email",

            }
        ))
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Your content here",

            }
        ))

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not "gmail" in email:
            raise forms.ValidationError("Sorry Your Email has to be a Gmail")
        return email
