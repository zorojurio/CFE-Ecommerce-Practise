from django.urls import path
from carts import views

app_name = 'cart'
urlpatterns = [
    path('', views.cart_home, name='home'),
    path('update/', views.cart_update, name='update'),
    path('checkout/', views.checkout_home, name='checkout'),
]
