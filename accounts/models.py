from django.db import models


class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BigIntegerField(default=True)
    update = models.DateField(auto_now=True)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email
