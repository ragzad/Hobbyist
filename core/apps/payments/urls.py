# apps/payments/urls.py
from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.payment_page, name='payment-page'),
    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
    path('success/', views.payment_success, name='payment-success'),
    path('cancel/', views.payment_cancel, name='payment-cancel'),
    path('webhook/', views.stripe_webhook, name='stripe-webhook'),
    path('create-checkout-session/premium/', views.create_premium_checkout_session, name='create-premium-checkout-session'),
    path('premium/success/', views.premium_success, name='premium-success'),
    path('premium/cancel/', views.premium_cancel, name='premium-cancel'),
]
