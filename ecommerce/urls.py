"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from accounts.views import LoginView, RegisterView, guest_register_view
from addresses.views import (checkout_address_create_view,
                             checkout_address_reuse_view)
from billing.views import payment_method, payment_method_create_view
from carts.views import cart_detail_api_view
from marketing.views import MarketingPreferenceUpdateView, MailChimpWebHookView

from .views import about_page, contact_page, home_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name="home"),
    path('about/', about_page, name="about"),
    path('contact/', contact_page, name="contact"),
    path('login/', LoginView.as_view(), name="login"),
    path('checkout/address/create/', checkout_address_create_view, name="checkout_address_create"),
    path('checkout/address/reuse/', checkout_address_reuse_view, name="checkout_address_reuse"),
    path('register/guest', guest_register_view, name="guest_register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('billing/payment-method/', payment_method, name="billing-payment-method"),
    path('billing/payment-method/create/', payment_method_create_view, name="billing-payment-method-end-point"),
    path("api/cart/", cart_detail_api_view, name="api-cart"),
    path('register/', RegisterView.as_view(), name="register"),
    path('products/', include('products.urls', namespace='products')),
    path('search/', include('search.urls', namespace='search')),
    path('settings/email/', MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),
    path('webhooks/mailchimp/', MailChimpWebHookView.as_view(), name='webhooks-mailchimp'),
    path('cart/', include('carts.urls', namespace='cart')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
