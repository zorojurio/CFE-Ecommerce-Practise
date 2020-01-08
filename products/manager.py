from django.db import models
from django.db.models import Q


class ProductQuerySet(models.query.QuerySet):
    def active(self):  # Products.objects.all().featured
        return self.filter(active=True)

    def featured(self):  # Products.objects.all().featured
        return self.filter(featured=True, active=True)

    def search(self, query):
        lookups = (
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(price__icontains=query) |
            Q(tag__title__icontains=query))
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):  # Product.objects.featured() give you all the featured ones
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        # self.get_queryset means Product.objects
        # so in here returning Products.objects.filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)
