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
        var form = $('#payment-form');
        var btnLoad = form.find(".paymentBtn")
        var btnLoadDefaultHtml = btnLoad.html()
        var btnLoadDefaultClasses = btnLoad.attr("class")

        form.on('submit', function (event) {
            event.preventDefault();
            var LoadTime = 1520
            var errorHtml = "<i class='fa fa-warning ' ></i> Error Occured"
            var errorClasses = "btn btn-danger btn-md  mt-4 ml-2 disabled"
            var loadingHtml = "<i class='fa fa-spin fa-spinner'></i> Loading..."
            var loadingClasses = "btn btn-success mt-4 ml-2 disabled my-3"


            stripe.createToken(card).then(function (result) {
                if (result.error) {
                    // Inform the user if there was an error.
                    var errorElement = $('#card-errors');
                    errorElement.textContent = result.error.message;
                    displayBtnStatus(
                        btnLoad,
                        errorHtml,
                        errorClasses,
                        1000,

                    )

                } else {
                    // Send the token to your server.
                    stripeTokenHandler(nextUrl, result.token);
                    displayBtnStatus(
                        btnLoad,
                        loadingHtml,
                        loadingClasses,
                        2000,

                    )

                }
            });
        });

        function displayBtnStatus(element, newHtml, newClasses, loadTime) {

            if (!loadTime) {
                loadTime = 1500
            }

            element.html(newHtml)
            element.removeClass(btnLoadDefaultClasses)
            element.addClass(newClasses)
            return setTimeout(function () {
                element.html(btnLoadDefaultHtml)
                element.removeClass(newClasses)
                element.addClass(btnLoadDefaultClasses)
            }, loadTime)

        }


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
                    btnLoad.html(btnLoadDefaultHtml)
                    btnLoad.attr("class", btnLoadDefaultClasses)
                    redirectToNext(nextUrl, 1500)

                },
                error: function (error) {
                    $.alert({ title: "An error Occured", content: "Please try adding Your card" })

                }
            })
        }
    }
})
