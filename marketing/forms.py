from django import forms
from marketing.models import MarketingPreference


class MarketingPreferenceForm(forms.ModelForm):
    """Form definition for MarketingPreference."""
    subscribed = forms.BooleanField(label='Subscribe Us for more exclusive products?', required=False)

    class Meta:
        """Meta definition for MarketingPreferenceform."""

        model = MarketingPreference
        fields = [
            'subscribed',
        ]
