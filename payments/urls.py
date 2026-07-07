from django.urls import path

from . import views

urlpatterns = [
    path('config/', views.stripe_config),
    path('create-checkout-session/<price>/', views.create_checkout_session),
    path('success/', views.success),
    path('cancelled/', views.cancelled),
    path('stripe-webhook/', views.stripe_webhook),

    path('cancel_subscription/', views.cancel_subscription, name='cancel_subscription'),
]