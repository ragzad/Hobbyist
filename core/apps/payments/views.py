import stripe
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from apps.users.models import Profile

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def payment_page(request):
    """
    Renders the page where the user can choose to upgrade.
    """
    context = {'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY}
    return render(request, 'payments/payment_page.html', context)

@login_required
def create_checkout_session(request):
    """
    Creates a Stripe Checkout session and redirects the user to Stripe's payment page.
    """
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'gbp',
                    'product_data': {
                        'name': 'Premium Account',
                    },
                    'unit_amount': 500,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('payments:payment-success')),
            cancel_url=request.build_absolute_uri(reverse('payments:payment-cancel')),
            client_reference_id=request.user.id,
        )
        return redirect(session.url, code=303)
    except Exception as e:
        return HttpResponse("Error: " + str(e), status=500)

@login_required
def payment_success(request):
    return render(request, 'payments/payment_success.html')

@login_required
def payment_cancel(request):
    return render(request, 'payments/payment_cancel.html')

@csrf_exempt
def stripe_webhook(request):
    """
    Listens for events from Stripe and updates the user's profile on success.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session.get('client_reference_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                # Use get_or_create to handle cases where a profile might not exist yet
                profile, created = Profile.objects.get_or_create(user=user)
                profile.is_premium = True
                profile.save()
            except User.DoesNotExist:
                return HttpResponse(status=404)

    # Passed signature verification
    return HttpResponse(status=200)

def create_premium_checkout_session(request):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Hobbyist Premium',
                },
                'unit_amount': 999, # This is $9.99
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payments:premium-success')),
        cancel_url=request.build_absolute_uri(reverse('payments:premium-cancel')),
        client_reference_id=request.user.id
    )
    return redirect(session.url, code=303)

def premium_success(request):
    # This is where you update the user's profile
    user = request.user
    user.profile.is_premium = True
    user.profile.save()
    return render(request, 'payments/payment_success.html')

def premium_cancel(request):
    return render(request, 'payments/payment_cancel.html')