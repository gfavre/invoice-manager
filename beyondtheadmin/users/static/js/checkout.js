console.log("Sanity check!");
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

fetch("/users/config/",)
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
      let form_data = {'code': document.querySelector('select[name="code"]').value};
      fetch("/users/create-checkout-session/", {
        method: 'POST',
        mode: 'cors',
        credentials: 'same-origin',
        body: JSON.stringify(form_data),
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,


        },
      }).then((result) => {
              console.log("got session id");

          return result.json();
      }).then((data) => {
        // Redirect to Stripe Checkout
          return stripe.redirectToCheckout({sessionId: data.sessionId})
      }).then((res) => {
          console.log(res);
      });
    });
  });
