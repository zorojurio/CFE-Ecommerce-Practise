from django.db import models
from billing.models import BillingProfile

ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)


class Address(models.Model):
    # one billing profile can have multiple addresses
    billing_profile = models.ForeignKey(
        BillingProfile, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPES)
    address_line1 = models.CharField(max_length=250)
    address_line2 = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=250)

    def __str__(self):
        return str(self.billing_profile)
        # return the str representatiom of the billing profile which is the email

    def get_address(self):
        return f"{self.address_line1}, {self.address_line2}, {self.city}, {self.state} {self.postal_code}, {self.country}"
