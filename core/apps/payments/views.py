# apps/payments/views.py
import stripe
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def payment_page(request):
    """
    Renders the page where the user can choose to upgrade.
    """
    # Pass the publishable key to the template
    context = {'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY}
    return render(request, 'payments/payment_page.html', context)

@login_required
def create_checkout_session(request):
    """
    Creates a Stripe Checkout session and redirects the user to Stripe's payment page.
    """
    try:
        # Create a new Checkout Session for the order
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'gbp', 
                    'product_data': {
                        'name': 'Premium Account',
                    },
                    'unit_amount': 500,  # Price in pence (£5.00)
                },
                'quantity': 1,
            }],
            mode='payment',
            # These are the URLs Stripe will redirect to on success or failure
            success_url=request.build_absolute_uri(reverse('payments:payment-success')),
            cancel_url=request.build_absolute_uri(reverse('payments:payment-cancel')),
            # We can pass the user's ID to the session to identify them in the webhook later
            client_reference_id=request.user.id,
        )
        return redirect(session.url, code=303)
    except Exception as e:
        return str(e)

# These views are for the pages the user sees after payment
@login_required
def payment_success(request):
    return render(request, 'payments/payment_success.html')

@login_required
def payment_cancel(request):
    return render(request, 'payments/payment_cancel.html')