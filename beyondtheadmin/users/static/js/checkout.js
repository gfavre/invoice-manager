console.log("Sanity check!");


fetch("/users/config/", )
  .then((result) => {
      return result.json();
    }
  )
  .then((data) => {
    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);
    document.querySelector("#checkout-and-portal-button").addEventListener("click", (evt) => {
      evt.stopPropagation();
      // Get Checkout Session ID
      fetch("/users/create-checkout-session/")
        .then((result) => {
          console.log(result.json())
          return result.json();
        })
        .then((data) => {
          console.log(data);
          // Redirect to Stripe Checkout
          return stripe.redirectToCheckout({sessionId: data.sessionId})
        })
        .then((res) => {
          console.log(res);
        });
    });
  });
