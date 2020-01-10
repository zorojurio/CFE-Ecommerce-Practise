from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from accounts.models import GuestEmail
User = get_user_model()

# anon user can have multiple billin profile and
# registered user can have only one billing profile


class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        if user.is_authenticated:
            if user.email:  # user is authenticated and he has an active email
                obj, created = self.model.objects.get_or_create(
                    user=user, email=user.email)

        elif guest_email_id is not None:
            guest_email_obj = GuestEmail.objects.get(
                id=guest_email_id)
            obj, created = self.model.objects.get_or_create(
                email=guest_email_obj.email)
        else:
            pass
        return obj, created


class BillingProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    # all the guest users are not active is the logic
    active = models.BooleanField(default=True)
    update = models.DateField(auto_now=True)
    timestamp = models.DateField(auto_now_add=True)
    # customer id of the stripe

    objects = BillingProfileManager()

    def __str__(self):
        return self.email


def user_created_receiever(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.create(user=instance, email=instance.email)


post_save.connect(user_created_receiever, sender=User)
