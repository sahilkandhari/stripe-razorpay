import os
import stripe
from flask import Flask, jsonify, render_template, request
import razorpay
import json


app = Flask(__name__)


#app = Flask(__name__,static_folder = "static", static_url_path='')
razorpay_client = razorpay.Client(auth=("rzp_test_8ydfJQKGSKoloz", "7LNONq8PYWjg4ImLujHDxpst"))
order_id = ''
params_dict = {}

'''
razorpay_keys = {
    "key_id" : os.environ["RZRP_KEY_ID"],
    "key" : os.environ["RZRP_KEY"]
}
'''

stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
    "endpoint_secret": os.environ["STRIPE_ENDPOINT_SECRET"],
}

stripe.api_key = stripe_keys["secret_key"]



def app_create():
    order_amount = 50000
    order_currency = 'INR'
    order_receipt = 'order_rcptid_100'
    notes = {'Shipping address': 'Pune, Maharashtra'}
    something = razorpay_client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes))
    return something['id']



def success():
    return render_template("success.html")


def cancelled():
    return render_template("cancelled.html")


'''
@app.route('/charge', methods=['POST'])
def rzrp_charge():
    amount = 5100
    payment_id = request.form['razorpay_payment_id']
    razorpay_client.payment.capture(payment_id, amount)
    return json.dumps(razorpay_client.payment.fetch(payment_id))
'''

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)


@app.route("/create-checkout-session")
def create_checkout_session():
    domain_url = "http://localhost:5000/"
    stripe.api_key = stripe_keys["secret_key"]

    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [payment_intent_data] - lets capture the payment later
        # [customer_email] - lets you prefill the email input in the form
        # For full details see https:#stripe.com/docs/api/checkout/sessions/create

        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "cancelled",
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "name": "T-shirt",
                    "quantity": 1,
                    "currency": "inr",
                    "amount": "2000",
                }
            ]
        )
        return jsonify({"sessionId": checkout_session["id"]})
    except Exception as e:
        return jsonify(error=str(e)), 403



def handle_checkout_session(session):
    print("Payment was successful.")
    # TODO: run some custom code here


@app.route("/success")
def success_redirect():
    success()


@app.route("/cancelled")
def cancelled_redirect():
    cancelled()



@app.route('/razorpay')
def app_pay():

    order_id = app_create()
    params_dict['razorpay_order_id'] = order_id


    razrp_config = {
        "options" : {
                        "key": "rzp_test_8ydfJQKGSKoloz",
                        "amount": "50000",
                        "currency": "INR",
                        "name": "BCT",
                        "description": "Test Transaction",
                        "order_id": order_id,
                        "callback_url": "http://127.0.0.1:5000/checkout",
                        "notes": {
                                    "address": "Razorpay Corporate Office"
                                },
                        "theme": {
                                "color": "#3399cc"
                            } 
                }
    }
    return jsonify(razrp_config)


@app.route('/checkout', methods=['POST'])
def app_charge():
    amount = 50000
    payment_id = request.form['razorpay_payment_id']
    signature = request.form['razorpay_signature']
    
    params_dict['razorpay_payment_id'] = payment_id
    params_dict['razorpay_signature'] = signature

    result = razorpay_client.utility.verify_payment_signature(params_dict)

    if result == None:
        success()
    else:
        cancelled()



if __name__ == "__main__":
    app.run()
