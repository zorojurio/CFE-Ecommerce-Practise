from django.db import models
from django.db.models.signals import pre_save

from ecommerce.utils import unique_slug_generator
from products.models import Product


class Tag(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    Products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.title


def tag_pre_save_receiecer(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(receiver=tag_pre_save_receiecer, sender=Tag)
