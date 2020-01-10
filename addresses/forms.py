from django import forms
from addresses.models import Address


class AddressForm(forms.ModelForm):
    """Form definition for Address."""

    class Meta:
        """Meta definition for Addressform."""

        model = Address
        fields = ['address_line1', 'address_line2', 'city',
                  'state', 'country', 'postal_code', ]
