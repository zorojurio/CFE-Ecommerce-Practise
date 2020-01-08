from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
User = get_user_model()

# anon user can have multiple billin profile and
# registered user can have only one billing profile


class BillingProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    # all the guest users are not active is the logic
    active = models.BooleanField(default=True)
    update = models.DateField(auto_now=True)
    timestamp = models.DateField(auto_now_add=True)
    # customer id of the stripe

    def __str__(self):
        return self.email


def user_created_receiever(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.create(user=instance, email=instance.email)


post_save.connect(user_created_receiever, sender=User)
