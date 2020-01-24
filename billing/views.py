from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.http import is_safe_url
from billing.models import BillingProfile, Card
from django.conf import settings
import stripe

STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY")
stripe.api_key = STRIPE_SECRET_KEY


def payment_method(request):

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect("cart:home")
    next_url = None
    next_ = request.GET.get("next")
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    context = {
        'publish_key': STRIPE_PUB_KEY,
        'next_url': next_url,
    }
    return render(request, template_name='billing/payment-method.html', context=context)


def payment_method_create_view(request):
    if request.method == "POST" and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({"message": "Cannot find this user"}, status_code=401)
        token = request.POST.get("token")
        if token is not None:
            new_card_obj = Card.objects.add_new(billing_profile, token)

        return JsonResponse({"message": "Success! Your card was added."})
    return HttpResponse({"error": "Try again"}, status_code=401)
