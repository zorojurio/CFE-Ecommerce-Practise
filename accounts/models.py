from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")

        user_obj = self.model(
            email=self.normalize_email(email)
        )
        user_obj.set_password(password)  # change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []  # ['full_name'] #python manage.py createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_fullname(self):
        return self.email

    def get_short_name(self):
        return self.email

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BigIntegerField(default=True)
    update = models.DateField(auto_now=True)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email
