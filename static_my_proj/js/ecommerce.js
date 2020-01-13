$(document).ready(function () {
    // contact form handler
    var contactForm = $(".contact-form")
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndpoint = contactForm.attr("action")


    function displaySubmitting(SubmitBtn, defaultText, doSubmit) {
        if (doSubmit) {
            SubmitBtn.addClass("disabled")
            SubmitBtn.html("<i class='fa fa-spin fa-spinner'></i> Submitting...")
        } else {
            SubmitBtn.removeClass("disabled")
            SubmitBtn.html(defaultText)
        }
    }

    contactForm.submit(function (event) {
        event.preventDefault()
        var contactFormSubmitBtn = contactForm.find("[type='submit']")
        var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()
        var contactFormData = contactForm.serialize()
        var thisForm = $(this)
        console.log("Success")
        displaySubmitting(contactFormSubmitBtn, "", true) // adding disabled
        $.ajax({
            method: contactFormMethod,
            url: contactFormEndpoint,
            data: contactFormData,

            success: function (data) {
                thisForm[0].reset()
                $.alert({
                    title: 'Success!',
                    content: data.message,
                    theme: 'supervan',
                });
                setTimeout(function () {
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
                }, 2000) // remove class after 2 seconds
            },
            error: function (error) {
                console.log(error.responseJSON)
                var jsonData = error.responseJSON
                var msg = ""
                $.each(jsonData, function (key, value) { // Json data is a dictionray thats y 
                    msg += key + ": " + value[0].message + "<br/>"
                    console.log(key)
                    console.log(value[0])
                })

                $.alert({
                    title: 'Error!',
                    content: msg,
                    theme: 'supervan',
                });
                setTimeout(function () {
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
                }, 2000) // remove class after 2 seconds
            }
        })
    })

    // auto search
    var searchForm = $(".search-form")
    var searchInput = searchForm.find("[name='q']")
    var typingTimer;
    var typingInterval = 1500; //.5 seconds
    var searchBtn = searchForm.find("[type='submit']")
    // key released  
    searchInput.keyup(function (event) {
        clearTimeout(typingTimer)
        typingTimer = setTimeout(performSearch, typingInterval)
    })

    // key pressed
    searchInput.keydown(function (event) {
        clearTimeout(typingTimer)
    })

    function displaySearching() {
        searchBtn.addClass("disabled")
        searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching...")
    }

    function performSearch() {
        displaySearching()
        var query = searchInput.val()
        setTimeout(function () {
            window.location.href = '/search/?q=' + query
        }, 1000)
    }




    // cart + Add products
    var ProductForm = $(".form-product-add-ajax")

    ProductForm.submit(function (event) {
        event.preventDefault();

        var thisForm = $(this) //grabing the data only specific to this form we are refering
        // var actionEndPoint = thisForm.attr("action");
        var actionEndPoint = thisForm.attr("data-endpoint")
        var httpMethod = thisForm.attr("method");
        var formData = thisForm.serialize(); // encode string for submission


        //sending data to back end
        // submiting the form throgh ajax
        $.ajax({
            url: actionEndPoint,
            method: httpMethod,
            data: formData,
            success: function (data) {
                var submitSpan = thisForm.find(".submit-span")
                console.log(submitSpan.html())
                //display data reciecved from back end
                if (data.added) {
                    submitSpan.html(' In cart <button class="btn btn-danger" type="submit"> Remove? </button>')
                } else {
                    submitSpan.html('<button class="btn btn-success" type="submit">Add to Cart</button>')
                }
                // navbar count
                var navbarCount = $(".navbar-cart-count")
                navbarCount.text(data.cartItemCount)


                //refresh the cart http://127.0.0.1:8000/cart/
                var currentPath = window.location.href
                if (currentPath.indexOf("cart") != - 1) {  //localhost/cart:8000
                    refreshCart()
                }
                console.log(window.location.href.indexOf("cart"))
            },
            error: function (errorData) {
                $.alert({
                    title: 'Error!',
                    content: 'A Fucking Error has Occured !',
                    theme: 'supervan',
                });
                console.log("error")
                console.log(errorData)
            },
        })

    })

    function refreshCart() {
        console.log("in current Cart")
        var cartTable = $(".cart-table")
        var cartBody = cartTable.find(".cart-body")
        //cartBody.html("<h1> Changed MF </h1>")
        var productsRows = cartBody.find(".cart-products")
        var currentUrl = window.location.href

        var refreshCartUrl = '/api/cart/'
        var refreshCartMethod = "GET" // refresh using the POSTed backend data
        var data = {}

        $.ajax({
            url: refreshCartUrl,
            method: refreshCartMethod,
            data: data,
            success: function (data) {
                var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
                if (data.products.length > 0) {
                    productsRows.html(' ')
                    i = data.products.length
                    $.each(data.products, function (index, value) {
                        var newCartItemRemove = hiddenCartItemRemoveForm.clone()
                        newCartItemRemove.css("display", "block")
                        newCartItemRemove.find(".cart-item-product-id").val(value.id)

                        cartBody.prepend("<tr><th scope='row'> " + i + "</th><td> <a href='" + value.url + "'>" + value.name + " </a>" + newCartItemRemove.html() + "</td><td>" + value.price + "</td></tr>")
                        i--
                    })

                    cartBody.find(".cart-subtotal").text(data.subtotal)
                    cartBody.find(".cart-total").text(data.total)
                } else {
                    // when there are no items in the cart it refreshes automatically because of the false condition
                    window.location.href = currentUrl
                }
            },
            error: function (errorData) {
                $.alert({
                    title: 'Error!',
                    content: 'A Fucking Error has Occured !',
                    theme: 'supervan',
                });
                console.log("error")
                console.log(errorData)
            },

        })
    }
})