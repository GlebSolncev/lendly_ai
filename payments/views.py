from datetime import timedelta, datetime
import json
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import stripe
import logging
from payments.models import Subscription, Payment
from user.models import User

logger = logging.getLogger(__name__)

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request, price):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'not_auth'})

        domain_url = settings.DOMAIN_URL
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'], #, 'paypal'
                mode='subscription',
                allow_promotion_codes ='true',
                line_items=[
                    {
                        "price": price,
                        'quantity': 1,
                    }
                ],
                client_reference_id=request.user.id,
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def stripe_webhook(request):
    
    # print(request.META['HTTP_STRIPE_SIGNATURE'])
    # breakpoint()

    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET

    # live    
    # payload = request.body
    # sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    # print(payload)

    # try:
    #     event = stripe.Webhook.construct_event(
    #         payload, sig_header, endpoint_secret
    #     )
    # except ValueError as e:
    #     print('val')
    #     print(e)
    #     return HttpResponse(status=400)
    # except stripe.error.SignatureVerificationError as e:
    #     print('verif')
    #     print(e)
    #     return HttpResponse(status=400)
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
        json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)


    if event['type'] == 'checkout.session.completed':
        result = stripe.Subscription.retrieve(event['data']['object']['subscription'])

        product_id = result['items']['data'][0]['price']['product']
        
        # Fetch details of the product using the product ID
        product = stripe.Product.retrieve(product_id)
        
        user = User.objects.get(id=event['data']['object']['client_reference_id'])

        payment = Payment(  
            subscription_id=result['id'],
            date=datetime.utcfromtimestamp(result['current_period_end']),
            user=user,
            subscription_object=Subscription.objects.get(title=product['name']),
        )
        payment.save()
        user.subscription = payment
        user.save()
    if event['type'] == 'invoice.paid':
        if event['data']['object']['billing_reason'] != 'subscription_create':
            try:
                payment = Payment.objects.get(
                    subscription_id=event['data']['object']['lines']['data'][0]['subscription']
                )
            except Payment.DoesNotExist:
                return HttpResponse(status=404)
            payment.date = datetime.utcfromtimestamp(event['data']['object']['lines']['data'][0]['period']['end'])
            payment.save()

    return HttpResponse(status=200)


def success(request):
    return render(request, 'success.html')


def cancelled(request):
    return render(request, 'cancelled.html')


def cancel_subscription(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    result = stripe.Subscription.delete(request.user.subscription.subscription_id)
    request.user.subscription.canceled = True
    request.user.subscription.save()

    request.user.content_gen_count = 0
    request.user.image_gen_count = 0
    request.user.logo_gen_count = 0
    request.user.seokeyword_gen_count = 0
    request.user.projectsCount = 0
    request.user.save()


    return redirect(request.META.get('HTTP_REFERER'))
