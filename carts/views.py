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
    # if there are no items in the cart send back to the cart form to add items
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")
    else:  # if the cart has items in it
        order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
        # create an order using the cart instance
        user = request.user
        billing_profile = None
        login_form = LoginForm()
        guest_form = GuestForm()
        guest_email_id = request.session.get('guest_email_id')

        if user.is_authenticated:
            if user.email:
                billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(
                    user=user, email=user.email)
        elif guest_email_id is not None:
            guest_email_obj = GuestEmail.objects.get(
                id=guest_email_id)
            billing_profile, billing_guest_profile_created = BillingProfile.objects.get_or_create(
                email=guest_email_obj.email)
        else:
            pass
    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
    }
    return render(request, template_name='carts/checkout.html', context=context)
