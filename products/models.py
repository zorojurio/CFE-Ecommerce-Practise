import os
import random

from django.db import models
# righ before its going to save in the data base it going to do something
from django.db.models.signals import pre_save
from django.urls import reverse

from products.manager import ProductManager, ProductQuerySet

from ecommerce.utils import unique_slug_generator


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):

    new_filename = random.randint(1, 391541656)
    name, ext = get_filename_ext(filename)

    final_filename = f"{new_filename}{ext}"
    return f"produts/{new_filename}/{final_filename}"


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2, default=39.99)
    image = models.ImageField(
        upload_to=upload_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    slug = models.SlugField(blank=True, unique=True)
    timestamp = models.DateField(auto_now_add=True)

    objects = ProductManager()

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


# beffore the mddel is saved in to the database uniques slug is generated
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)
