from django.shortcuts import render
from products.models import Product
from django.views.generic import ListView


class SearchProductListView(ListView):
    template_name = "search/view.html"

    def get_queryset(self):
        query = self.request.GET.get('q', None)

        print(query)
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.featured()

        # __icontains >> field contains this
        # __iexact >> field is exacly this
