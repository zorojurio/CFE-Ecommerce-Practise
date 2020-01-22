from django.shortcuts import render, get_object_or_404
from .models import Product
from django.views.generic import ListView, DetailView
from django.http import Http404
from carts.models import Cart

from analytics.mixins import ObjectViewedMixin


class ProductListView(ListView):
    queryset = Product.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView,
                        self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context


class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    template_name = "products/product_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView,
                        self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')

        # instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product.objects.get(slug=slug, active=True)

        except Product.DoesNotExist:
            raise Http404("Product Not Found Fucker")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        # object_viewed_signal.send(instance.__class__, instance, self.request)
        return instance


# def product_list_view(request):
#     queryset = Product.objects.all()
#     context = {
#         "qs": queryset
#     }
#     return render(request, "products/product_list.html", context=context)


# class ProductDetailView(DetailView):
#     queryset = Product.objects.all()

#     def get_context_data(self, **kwargs):
#         context = super(ProductDetailView, self).get_context_data(**kwargs)
#         print(context['object.title'])
#         return context

#     def get_object(self, *args, **kwargs):
#         request = self.request
#         pk = self.kwargs.get("pk")
#         instance = Product.objects.get_by_id(pk)
#         if instance is None:
#             raise Http404("Product Doest Exist")
#         return instance


# def product_detail_view(request, pk, *args, **kwargs):
#     print(args)
#     print(kwargs)
#     instance = Product.objects.get_by_id(pk)
#     if instance is None:
#         raise Http404("Product Doesnt exist")
#     context = {
#         "object": instance
#     }
#     print(instance)
#     return render(request, "products/product_detail.html", context=context)


# class ProductFeaturedListView(ListView):
#     template_name = "products/product_list.html"

#     def get_queryset(self, *args, **kwargs):
#         request = self.request
#         return Product.objects.all().featured()


# class ProductFeaturedDetailView(DetailView):
#     template_name = "products/featured-detail.html"
#     queryset = Product.objects.all().featured()
