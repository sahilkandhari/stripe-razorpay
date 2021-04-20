document.getElementById("submitBtn").addEventListener("click", () => {
  let radioVal;

  radioVal = document.querySelector('input[name= "select"]:checked').value;
  console.log(radioVal);

  if(radioVal == 'strp') {
  
// Get Stripe publishable key
    fetch('/config')
    .then((result) => { return result.json(); })
    .then((data) => {
      // Initialize Stripe.js
      const stripe = Stripe(data.publicKey);

  // Event handler
    // Get Checkout Session ID
      fetch('/create-checkout-session')
      .then((result) => { return result.json(); })
      .then((data) => {
        console.log(data);
      // Redirect to Stripe Checkout
        return stripe.redirectToCheckout({sessionId: data.sessionId})
      })
      .then((res) => {
        console.log(res);
      });
  });

}
else if (radioVal == 'rzrp') {
  fetch('/razorpay')
  .then((result) => { return result.json(); })
  .then((data) => {
    // Initialize js
    console.log(data)
    const rzp1 = new Razorpay(data.options);
      rzp1.open()
      .then((res) => {
          console.log(res);
          // Redirect 
    });
  });
}

});
