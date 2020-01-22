from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from .signals import object_viewed_signal
from .utils import get_client_ip
from django.contrib.sessions.models import Session
from accounts.signals import user_logged_in
from django.db.models.signals import post_save
from django.conf import settings

User = get_user_model()
FORCE_SESSION_TO_THREE = getattr(settings, "FORCE_SESSION_TO_THREE", False)
FORCE_INACTIVE_USER_ENDSESSION = getattr(settings, "FORCE_INACTIVE_USER_ENDSESSION", False)


class ObjectViewed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)  # Order #Product
    object_id = models.PositiveIntegerField()  # Product ID
    content_object = GenericForeignKey('content_type', 'object_id')  # Product instance
    ip_address = models.CharField(max_length=220, blank=True, null=True)  # IP Field
    timestamp = models.DateTimeField(auto_now_add=True)
    user_session_key = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s viewed on %s" % (self.content_object, self.timestamp)

    class Meta:
        ordering = ['-timestamp']  # most recent saved show up first
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Objects viewed'


def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)  # instance.__class__
    user_session_key = request.session.session_key
    try:
        ip_address = get_client_ip(request)
        user_session_key = request.session.session_key
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
    except:
        pass

    new_view_instance, created = ObjectViewed.objects.get_or_create(
        user=user,
        content_type=c_type,
        object_id=instance.id,
        ip_address=ip_address,
        user_session_key=user_session_key
    )


object_viewed_signal.connect(object_viewed_receiver)


class UserSession(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)  # User instance instance.id
    ip_address = models.CharField(max_length=220, blank=True, null=True)  # IP Field
    session_key = models.CharField(max_length=100, blank=True, null=True)  # min 50
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    ended = models.BooleanField(default=False)

    def end_session(self):
        session_key = self.session_key

        try:
            self.active = False
            self.ended = True
            self.save()
            Session.objects.get(pk=session_key).delete()
        except:
            pass
        return self.ended


def post_save_deactivated_user(sender, instance, created, *args, **kwargs):
    """ As soon as the user is deactivated, dreactivate all previous user sessions """
    if not created:
        if instance.active == False:
            qs = UserSession.objects.filter(user=instance, ended=False, active=True)
            for i in qs:
                i.end_session()


if FORCE_INACTIVE_USER_ENDSESSION:
    post_save.connect(post_save_deactivated_user, sender=User)


def post_save_delete_old_session_receiver(sender, instance, created, *args, **kwargs):
    """ As soon as the user logged in agiain deactivate all previous user_sessions """

    if created:
        qs = UserSession.objects.exclude(id=instance.id).filter(user=instance.user, ended=False,)
        for i in qs:
            i.end_session()
    if not instance.active and not instance.ended:
        instance.end_session()


if FORCE_SESSION_TO_THREE:
    post_save.connect(post_save_delete_old_session_receiver, sender=UserSession)


def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    """ as soon as the user logged in create a UserSession Object """
    user = instance
    ip_address = get_client_ip(request)
    session_key = request.session.session_key

    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key
    )


user_logged_in.connect(user_logged_in_receiver)
