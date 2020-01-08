from django.shortcuts import render, get_object_or_404, redirect
from carts.models import Cart
from products.models import Product
from orders.models import Order
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from accounts.models import GuestEmail


def cart_home(request):  # url >> /cart/
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    context = {
        "cart": cart_obj,
    }
    return render(request, template_name="carts/home.html", context=context)


def cart_update(request):  # url >> /cart/update # add to cart remove  cart
    print(request.POST)
    product_id = request.POST.get("product_id")
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Message Product is gone")
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)
        request.session['cart_items'] = cart_obj.products.count()
    return redirect("cart:home")


def checkout_home(request):  # url >> /cart/checkout
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    # if there are no items in the cart send back cart home
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")
    login_form = LoginForm()  # create an order using the cart instance
    guest_form = GuestForm()

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
        request)  # both login and guest checkouts are handeled in manager
    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(
            billing_profile, cart_obj)

    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
    }
    return render(request, template_name='carts/checkout.html', context=context)
