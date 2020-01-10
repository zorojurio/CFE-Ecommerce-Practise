from django.shortcuts import render, redirect
from addresses.forms import AddressForm
from django.utils.http import is_safe_url
from billing.models import BillingProfile
from addresses.models import Address


def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post
    if form.is_valid():
        instance = form.save(commit=False)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

        if billing_profile is not None:
            instance.billing_profile = billing_profile
            address_type = request.POST.get('address_type', 'shipping')
            instance.address_type = address_type
            instance.save()
            request.session[address_type+"_address_id"] = instance.id
        else:
            print("error")
            return redirect("cart:checkout")
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
    return redirect('cart:checkout')


def checkout_address_reuse_view(request):

    if request.user.is_authenticated:
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post
        if request.method == "POST":
            print(request.POST)
            shipping_address = request.POST.get('shipping_address', None)
            address_type = request.POST.get('address_type', 'shipping')
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
            if shipping_address is not None:
                qs = Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
                if qs.exists():
                    request.session[address_type+"_address_id"] = shipping_address
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
    return redirect('cart:checkout')
