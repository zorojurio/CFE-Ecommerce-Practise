from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from .utils import MailChimp


class MarketingPreference(models.Model):
    """Model definition for MarketingPreference."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscribed = models.BooleanField(default=True)
    mailchimp_subscribed = models.NullBooleanField(blank=True)
    mailchimp_msg = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Unicode representation of MarketingPreference."""
        return self.user.email


def marketing_preference_create_receiver(sender, instance, created, *args, **kwargs):
    """ As soon as the Marketing preference object is created User
        will be added to the mail chimp audience through the API of mail chimp
     """
    if created:
        status_code, response_data = MailChimp().add_email(instance.user.email)
        print(status_code, response_data)


post_save.connect(marketing_preference_create_receiver, sender=MarketingPreference)


def marketing_preference_update_receiver(sender, instance, *args, **kwargs):
    if instance.subscribed != instance.mailchimp_subscribed:
        if instance.subscribed:
            status_code, response_data = MailChimp().subscribe(instance.user.email)
        else:
            status_code, response_data = MailChimp().unsubscribe(instance.user.email)

        if response_data["status"] == "subscribed":
            instance.subscribed = True
            instance.mailchimp_subscribed = True
            instance.mailchimp_msg = response_data
        else:
            instance.subscribed = False
            instance.mailchimp_subscribed = False
            instance.mailchimp_msg = response_data


pre_save.connect(marketing_preference_update_receiver, sender=MarketingPreference)


def make_marketing_pref(sender, instance, created, *args, **kwargs):
    """As soon as the user is created marketing preference object is created"""
    if created:
        MarketingPreference.objects.get_or_create(user=instance)


post_save.connect(make_marketing_pref, sender=settings.AUTH_USER_MODEL)
