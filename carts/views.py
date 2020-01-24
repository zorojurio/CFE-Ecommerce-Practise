from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from accounts.forms import GuestForm, LoginForm
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address
from billing.models import BillingProfile
from carts.models import Cart
from orders.models import Order
from products.models import Product
from django.conf import settings
import stripe

STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY")
stripe.api_key = STRIPE_SECRET_KEY


# template tag items >> json response items
# seperate view for JSON respose so it can handle the data without being refreshed
def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
        "url": x.get_absolute_url(),
        "id": x.id,
        "name": x.title,
        "price": x.price,
    } for x in cart_obj.products.all()]
    cart_data = {"products": products, "subtotal": cart_obj.subtotal, "total": cart_obj.total}
    return JsonResponse(cart_data)


def cart_home(request):  # url >> /cart/
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    context = {
        "cart": cart_obj,
    }
    return render(request, template_name="carts/home.html", context=context)


def cart_update(request):  # url >> /cart/update # add to cart remove  cart

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
            added = False
        else:
            cart_obj.products.add(product_obj)
            added = True
        request.session['cart_items'] = cart_obj.products.count()
        if request.is_ajax():
            print("ajax")
            json_data = {
                "added": added,  # add to card is clicked so added is true. removed is false
                "removed": not added,
                # if the remove from cart is clicked added is false hense not added is true
                "cartItemCount": cart_obj.products.count()
            }
            return JsonResponse(json_data, status=200)
            # return JsonResponse({"message": "Error  400"}, status=400)
    return redirect("cart:home")


def checkout_home(request):  # url >> /cart/checkout
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None

    # if there are no items in the cart send back cart home
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")

    login_form = LoginForm()  # create an order using the cart instance
    guest_form = GuestForm()

    address_form = AddressForm()

    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    has_card = False
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if billing_address_id or shipping_address_id:
            order_obj.save()
        has_card = billing_profile.has_card

    if request.method == "POST":
        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge, crg_msg = billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_paid()
                request.session['cart_items'] = 0

                del request.session['cart_id']
                if not billing_profile.user:
                    billing_profile.set_cards_inactive()
                return redirect("cart:success")
            else:
                print(crg_msg)
                return redirect("cart:checkout")
    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
        'address_form': address_form,
        'address_qs': address_qs,
        "has_card": has_card,
        "publish_key": STRIPE_PUB_KEY,

    }
    return render(request, template_name='carts/checkout.html', context=context)


def checkout_done_view(request):
    return render(request, template_name='carts/checkout-done.html')
# lolla
