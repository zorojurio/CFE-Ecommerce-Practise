from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from .forms import ContactForm
from django.contrib.auth import authenticate, login, get_user_model


def home_page(request):
    print(request.session.get("first_name", "unknown"))  # getter
    print(request.session.get("user"))  # getter
    context = {
        'title': "this is home",
        "content": "welcome to home page"
    }

    return render(request, "home.html", context=context)


def about_page(request):
    context = {
        "title": "about",
        "content": "welcome to about page"
    }
    return render(request, "home.html", context=context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        'title': "this is contact ",
        "content": "welcome to Contact page",
        "form": contact_form
    }
    print(request.POST)
    if request.method == "POST":
        if contact_form.is_valid():
            print(contact_form.cleaned_data)
            if request.is_ajax():
                return JsonResponse({"message": "Thank You For Your Submission"})  # converts dictionary into JSON

        if contact_form.errors:
            errors = contact_form.errors.as_json()  # this is already JSON FOmat hense HTTP response is used
            if request.is_ajax():
                return HttpResponse(errors, status=400, content_type='application/json')
    return render(request, "contact/view.html", context=context)
