$(document).ready(function () {
    var stripeFormModule = $(".stripe-payment-form") // where we going to add data 
    var stripeModuleToken = stripeFormModule.attr("data-token") // data token is the publishable key
    var stripeModuleNextUrl = stripeFormModule.attr("data-next-url") // data token is the publishable key
    var stripeModuleBtnTitle = stripeFormModule.attr("data-btn-title") || "Add card"


    var stripeTemplate = $.templates("#stripeTemplate") // tempalte object
    var stripeTemplateDataContext = { // template data
        pubKey: stripeModuleToken,
        nextUrl: stripeModuleNextUrl,
        btnTitle: stripeModuleBtnTitle
    }
    var stripeTemplateHtml = stripeTemplate.render(stripeTemplateDataContext) // adding data to the tempalte
    stripeFormModule.html(stripeTemplateHtml) // passing the template with data to the where we going to add

    // Create a Stripe client.
    var paymentForm = $(".payment-form")
    if (paymentForm.length > 1) {
        alert("Only one payment form is allowed")
        paymentForm.css("display", "None")
    } else {
        var pubKey = paymentForm.attr("data-token")
        var nextUrl = paymentForm.attr("data-next-url")
        var stripe = Stripe(pubKey);

        // Create an instance of Elements.
        var elements = stripe.elements();

        // Custom styling can be passed to options when creating an Element.
        // (Note that this demo uses a wider set of styles than the guide below.)
        var style = {
            base: {
                color: '#32325d',
                fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
                fontSmoothing: 'antialiased',
                fontSize: '16px',
                '::placeholder': {
                    color: '#aab7c4'
                }
            },
            invalid: {
                color: '#fa755a',
                iconColor: '#fa755a'
            }
        };

        // Create an instance of the card Element.
        var card = elements.create('card', { style: style });

        // Add an instance of the card Element into the `card-element` <div>.
        card.mount('#card-element');

        // Handle real-time validation errors from the card Element.
        card.addEventListener('change', function (event) {
            var displayError = document.getElementById('card-errors');
            if (event.error) {
                displayError.textContent = event.error.message;
            } else {
                displayError.textContent = '';
            }
        });

        // Handle form submission.
        var form = document.getElementById('payment-form');
        form.addEventListener('submit', function (event) {
            event.preventDefault();

            stripe.createToken(card).then(function (result) {
                if (result.error) {
                    // Inform the user if there was an error.
                    var errorElement = document.getElementById('card-errors');
                    errorElement.textContent = result.error.message;
                } else {
                    // Send the token to your server.
                    stripeTokenHandler(nextUrl, result.token);
                }
            });
        });

        function redirectToNext(nextPath, timeoffset) {
            // body...
            if (nextPath) {
                setTimeout(function () {
                    window.location.href = nextPath
                }, timeoffset)
            }
        }
        // Submit the form with the token ID.
        function stripeTokenHandler(nextUrl, token) {
            console.log(token.id)
            var paymentMethodEndPoint = "/billing/payment-method/create/"
            var data = {
                "token": token.id
            }
            $.ajax({
                data: data,
                method: "POST",
                url: paymentMethodEndPoint,
                success: function (data) {
                    console.log(data.message)
                    var successMsg = data.message || "Success your card was added"
                    card.clear()
                    if (nextUrl) {
                        successMsg = successMsg + "<br/><br/><i class='fa fa-spin fa-spinner'></i> Redirecting..."
                    }
                    if ($.alert) {
                        $.alert(successMsg)
                    } else {
                        alert(successMsg)
                    }
                    redirectToNext(nextUrl, 1500)

                },
                error: function (error) {
                    console.log("error")
                    console.log(error)

                }
            })
        }
    }
})
