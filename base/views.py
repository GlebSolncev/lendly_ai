from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from base.mail_service import mail_service
from base.models import Faq, Page, subscriberList
from payments.models import Subscription, Payment
from django.contrib.auth.models import AnonymousUser
import openai, re
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.http import HttpResponse
import time
from .seo_chatgpt import get_chat_response  # Import the function from your module
from .dall_e import dall_e  
from user.models import User

# midj funcs

BASE_URL = "https://api.thenextleg.io/v2"
AUTH_TOKEN = "746dfb8d-2a11-4034-90e1-53d363347c87"
AUTH_HEADERS = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/json",
}

def sleep(milliseconds):
    time.sleep(milliseconds / 1000)

def fetch_to_completion(message_id, retry_count, max_retry=200):
    image_res = requests.get(f"{BASE_URL}/message/{message_id}", headers=AUTH_HEADERS)
    image_response_data = image_res.json()

    if image_response_data["progress"] == "incomplete":
        raise Exception("Image generation failed")

    if retry_count > max_retry:
        raise Exception("Max retries exceeded")

    if image_response_data["progress"]:
        # print("---------------------")
        print(f'Progress: {image_response_data["progress"]}%')
        # print("---------------------")
        return image_response_data


    # sleep(5000)
    return fetch_to_completion(message_id, retry_count + 1)

def main(prompt=""):
    # Generate the image
    image_res = requests.post(
        f"{BASE_URL}/imagine", headers=AUTH_HEADERS, json={"msg": prompt}
    )
    image_response_data = image_res.json()
    print("\n=====================")
    print("IMAGE GENERATION MESSAGE DATA")
    print(image_response_data)
    print("=====================")

    return image_response_data
    # end

def button(button,button_id):
    variation_res = requests.post(
        f"{BASE_URL}/button",
        headers=AUTH_HEADERS,
        json={
            "button": button,
            "buttonMessageId": button_id,
        },
    )
    variation_response_data = variation_res.json()
    
    return variation_response_data



def index(request):
   # print(request.user)
    # print(request.user.id)
    # print(request.user.subscription_id)
    subscriptions = Subscription.objects.all()

    if isinstance(request.user, AnonymousUser):        
        context = {
            'subscriptions': subscriptions,
        }
    else:  # Remove the unnecessary colon after elif
        try:
            currPayment = Payment.objects.get(id=request.user.subscription_id)

            if currPayment.canceled:
                context = {
                    'subscriptions': subscriptions,
                    'currSubscription': 'FREE',
                    'guest': 'FREE',
                    'currSubscriptionClass': 'free',

                }

            else:
                currSubscription = Subscription.objects.get(id=currPayment.subscription_object_id).title
                currSubscriptionClass = Subscription.objects.get(id=currPayment.subscription_object_id).classname
                # print('payment')
                # print(currSubscription)

                context = {
                    'subscriptions': subscriptions,
                    'currSubscription': currSubscription,
                    'currSubscriptionClass': currSubscriptionClass,
                }    
        except Payment.DoesNotExist:
            context = {
                'subscriptions': subscriptions,
                'currSubscription': 'FREE',
                'currSubscriptionClass': 'free',
            }

    return render(request, 'base.html',context=context)


def support(request):
    if request.method == 'POST':
        mail_service.send_support_email(request.POST.get('name'),
                                        request.POST.get('email'),
                                        request.POST.get('message'))

    faqs = Faq.objects.all()
    context = {'faqs': faqs}
    return render(request, 'support.html', context=context)

def page(request, slug):
    page = Page.objects.get(slug=slug)
    return render(request, 'page.html', context={'page': page})

def about(request):
    return render(request, 'about.html')


def chat_view(request):
    if isinstance(request.user, AnonymousUser):  
        return redirect(reverse('login'))
    if request.user.subscription_id:
        
        currPayment = Payment.objects.get(id=request.user.subscription_id)
        if currPayment.canceled:
            return redirect(reverse('index') + '#pricingSection')
    else:
        return redirect(reverse('index') + '#pricingSection')


    if request.method == 'POST':

        current_user = request.user


        if isinstance(current_user, AnonymousUser):        
            return JsonResponse({'response': 'Login To Continue'})

        else:  # Remove the unnecessary colon after elif
            count = current_user.seokeyword_gen_count

            try:
                currPayment = Payment.objects.get(id=request.user.subscription_id)

                if currPayment.canceled:
                    if count < 0:
                        data = json.loads(request.body.decode('utf-8'))
                        user_input = data.get('user_input', '')  # Get the 'user_input' from the JSON data
                        response = get_chat_response(user_input)

                        current_user.seokeyword_gen_count = count + 1
                        current_user.save()
                        return JsonResponse({'response': response})
                    else: 
                        return JsonResponse({'response': 'Limit Reached <a href="https://landlyai.com/#pricingSection"><u>Upgrade plan to continue using.</u></a>'})


                else:
                    # currSubscription = Subscription.objects.get(id=currPayment.subscription_object_id).title
                    limit = Subscription.objects.get(id=currPayment.subscription_object_id).seokeyword_gen_limit
                     
                    if count < limit:
                        data = json.loads(request.body.decode('utf-8'))
                        user_input = data.get('user_input', '')  # Get the 'user_input' from the JSON data
                        response = get_chat_response(user_input)

                        current_user.seokeyword_gen_count = count + 1
                        current_user.save()
                        return JsonResponse({'response': response})
                    else: 
                        return JsonResponse({'response': 'Limit Reached <a href="https://landlyai.com/#pricingSection"><u>Upgrade plan to continue using.</u></a>'})

                    

            except Payment.DoesNotExist:
                if count < 5:
                    data = json.loads(request.body.decode('utf-8'))
                    user_input = data.get('user_input', '')  
                    response = get_chat_response(user_input)

                    current_user.seokeyword_gen_count = count + 1
                    current_user.save()
                    return JsonResponse({'response': response})
                else: 
                    return JsonResponse({'response': 'Limit Reached <a href="https://landlyai.com/#pricingSection"><u>Upgrade plan to continue using.</u></a>'})


        
    return render(request, 'seo_keyword.html')

def content_creator(request):
    if isinstance(request.user, AnonymousUser):  
        return redirect(reverse('login'))

    if request.user.subscription_id:
        
        currPayment = Payment.objects.get(id=request.user.subscription_id)
        if currPayment.canceled:
            return redirect(reverse('index') + '#pricingSection')

    else:
        return redirect(reverse('index') + '#pricingSection')

    if request.method == 'POST':


        current_user = request.user


        if isinstance(current_user, AnonymousUser):        
            return JsonResponse({'response': 'Login To Continue'})

        else:  # Remove the unnecessary colon after elif
            count = current_user.content_gen_count

            try:
                currPayment = Payment.objects.get(id=request.user.subscription_id)

                if currPayment.canceled:
                    if count < 0:
                        data = json.loads(request.body.decode('utf-8'))
                        user_input = data.get('user_input', '')  # Get the 'user_input' from the JSON data
                        response = get_chat_response(user_input)

                        current_user.content_gen_count = count + 1
                        current_user.save()
                        return JsonResponse({'response': response})
                    else: 
                        return JsonResponse({'response': 'Limit Reached <a href="https://landlyai.com/#pricingSection"><u>Upgrade plan to continue using.</u></a>'})


                else:
                    # currSubscription = Subscription.objects.get(id=currPayment.subscription_object_id).title
                    limit = Subscription.objects.get(id=currPayment.subscription_object_id).content_gen_limit
                     
                    if count < limit:
                        data = json.loads(request.body.decode('utf-8'))
                        user_input = data.get('user_input', '')  # Get the 'user_input' from the JSON data
                        response = get_chat_response(user_input)

                        current_user.content_gen_count = count + 1
                        current_user.save()
                        return JsonResponse({'response': response})
                    else: 
                        return JsonResponse({'response': 'Limit Reached <a href="https://landlyai.com/#pricingSection"><u>Upgrade plan to continue using.</u></a>'})

                    

            except Payment.DoesNotExist:
                if count < 5:
                    data = json.loads(request.body.decode('utf-8'))
                    user_input = data.get('user_input', '')  # Get the 'user_input' from the JSON data
                    response = get_chat_response(user_input)

                    current_user.content_gen_count = count + 1
                    current_user.save()
                    return JsonResponse({'response': response})
                else: 
                    return JsonResponse({'response': 'Limit Reached <a href="https://landlyai.com/#pricingSection"><u>Upgrade plan to continue using.</u></a>'})


        # data = json.loads(request.body.decode('utf-8'))
        # user_input = data.get('user_input', '')  # Get the 'user_input' from the JSON data
        # response = get_chat_response(user_input)
        # return JsonResponse({'response': response})
    
    return render(request, 'content_creator.html')


def image_generator(request):
    if isinstance(request.user, AnonymousUser):  
        return redirect(reverse('login'))


    if request.user.subscription_id:
    
        currPayment = Payment.objects.get(id=request.user.subscription_id)
        if currPayment.canceled:
            return redirect(reverse('index') + '#pricingSection')
    else:
        return redirect(reverse('index') + '#pricingSection')

    past_creations = request.user.generated_Images
    past_creations.reverse()
    
    # current_user = request.user 
    if request.method == 'POST':

        current_user = request.user

        if isinstance(current_user, AnonymousUser):        
            return JsonResponse({'response': 'Login To Continue'})

        else:  # Remove the unnecessary colon after elif
            count = current_user.image_gen_count

            try:
                currPayment = Payment.objects.get(id = current_user.subscription_id)
        
                if currPayment.canceled:
                    if count < 0:

                        data = json.loads(request.body.decode('utf-8'))
                        user_input = data.get('user_input', '')
                        genImg = dall_e(user_input)

                       

                        return JsonResponse({'response': f"{genImg}"})

                    else: 
                        return JsonResponse({'response': 'Limit Reached'})


                else:
                    # currSubscription = Subscription.objects.get(id=currPayment.subscription_object_id).title
                    limit = Subscription.objects.get(id=currPayment.subscription_object_id).image_gen_limit
                     
                    if count < limit:
                        data = json.loads(request.body.decode('utf-8'))
                        user_input = data.get('user_input', '')
                        genImg = dall_e(user_input)

                

                        return JsonResponse({'response': f"{genImg}"})

                    else: 
                        return JsonResponse({'response': 'Limit Reached'})

                    

            except Payment.DoesNotExist:
                if count < 12:
                    data = json.loads(request.body.decode('utf-8'))
                    user_input = data.get('user_input', '')
                    genImg = dall_e(user_input)

            

                    return JsonResponse({'response': f"{genImg}"})

                else: 
                    return JsonResponse({'response': 'Limit Reached'})


          


    return render(request, 'image_generator.html', {'past_creations':past_creations} )

def image_generator_periodic(request):
    past_creations = request.session.get('past_creations', [])


    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8'))
        message_id = data.get('message_id', '') 
        completed_image_data = fetch_to_completion(message_id, 0)

        print(completed_image_data)
        if completed_image_data['progress'] != 100:
            return JsonResponse({'image_urls' : completed_image_data['progressImageUrl'],'buttonMessageId' : '', 'progress': completed_image_data["progress"] })
        else:
            past_creations.append(completed_image_data)
            request.session['past_creations'] = past_creations
            past_creations_json = json.dumps(past_creations)
            return JsonResponse({'image_urls' : completed_image_data['response']['imageUrl'],'buttonMessageId' :  completed_image_data['response']['buttonMessageId'], 'progress': completed_image_data["progress"],'past_creations': past_creations_json })
        # return JsonResponse({'completed_image_data' : completed_image_data })
        

    return render(request, 'image_generator.html')

# logo ------------------- start

def logo_generator(request):
    if isinstance(request.user, AnonymousUser):  
        return redirect(reverse('login'))
    
    if request.user.subscription_id:
    
        currPayment = Payment.objects.get(id=request.user.subscription_id)
        if currPayment.canceled:
            return redirect(reverse('index') + '#pricingSection')
    else:
        return redirect(reverse('index') + '#pricingSection')

    past_creations = request.user.generated_Images_Logo
    past_creations.reverse()

    if request.method == 'POST':        
        current_user = request.user
        if isinstance(current_user, AnonymousUser):        
            return JsonResponse({'response': 'Login To Continue'})

        else:  # Remove the unnecessary colon after elif
            count = current_user.logo_gen_count

            try:
                currPayment = Payment.objects.get(id=request.user.subscription_id)

                if currPayment.canceled:
                    if count < 0:
                        data = json.loads(request.body.decode('utf-8'))
                        user_input = data.get('user_input', '')
                        genImg = dall_e(user_input)

                    

                        return JsonResponse({'response': f"{genImg}"})

                    else: 
                        return JsonResponse({'response': 'Limit Reached'})


                else:
                    # currSubscription = Subscription.objects.get(id=currPayment.subscription_object_id).title
                    limit = Subscription.objects.get(id=currPayment.subscription_object_id).logo_gen_limit
                     
                    if count < limit:
                        data = json.loads(request.body.decode('utf-8'))
                        user_input = data.get('user_input', '')
                        genImg = dall_e(user_input)

                      

                        return JsonResponse({'response': f"{genImg}"})

                    else: 
                        return JsonResponse({'response': 'Limit Reached'})

                    

            except Payment.DoesNotExist:
                if count < 4:
                    data = json.loads(request.body.decode('utf-8'))
                    user_input = data.get('user_input', '')
                    genImg = dall_e(user_input)

                

                    return JsonResponse({'response': f"{genImg}"})

                else: 
                    return JsonResponse({'response': 'Limit Reached'})

   
    return render(request, 'logo_generator.html', {'past_creations':past_creations} )



def logo_generator_periodic(request):
    past_creations_logo = request.session.get('past_creations_logo', [])


    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        message_id = data.get('message_id', '') 
        completed_image_data = fetch_to_completion(message_id, 0)

        print(completed_image_data)
        if completed_image_data['progress'] != 100:
            return JsonResponse({'image_urls' : completed_image_data['progressImageUrl'],'buttonMessageId' : '', 'progress': completed_image_data["progress"] })
        else:
            past_creations_logo.append(completed_image_data)
            request.session['past_creations_logo'] = past_creations_logo
            past_creations_json = json.dumps(past_creations_logo)
            return JsonResponse({'image_urls' : completed_image_data['response']['imageUrl'],'buttonMessageId' :  completed_image_data['response']['buttonMessageId'], 'progress': completed_image_data["progress"],'past_creations_logo': past_creations_json })
        # return JsonResponse({'completed_image_data' : completed_image_data })
        

    return render(request, 'logo_generator.html')

def underConstruction(request):
    return render(request, 'underConstruction.html')
    
def car_dealership(request):
    return render(request, 'subPages/car-dealership.html')

def display_ads(request):
    return render(request, 'subPages/display-ads.html')

def ecommerce_sales(request):
    return render(request, 'subPages/ecommerce-sales.html')

def education(request):
    return render(request, 'subPages/education.html')

def finance(request):
    return render(request, 'subPages/finance.html')

def games_and_entertainment(request):
    return render(request, 'subPages/games-and-entertainment.html')

def health_and_beauty(request):
    return render(request, 'subPages/health-and-beauty.html')

def insurance(request):
    return render(request, 'subPages/insurance.html')

def lead_generation(request):
    return render(request, 'subPages/lead-generation.html')

def marketing_and_advertising(request):
    return render(request, 'subPages/marketing-and-advertising.html')

def real_estate(request):
    return render(request, 'subPages/real-estate.html')

def retargeting(request):
    return render(request, 'subPages/retargeting.html')

def search_ads(request):
    return render(request, 'subPages/search-ads.html')

def social_ads(request):
    return render(request, 'subPages/social-ads.html')

def software_and_tech(request):
    return render(request, 'subPages/software-and-tech.html')

def sports_and_events(request):
    return render(request, 'subPages/sports-and-events.html')


# def indexTemp(request):
#     # print(request.user)
#     # print(request.user.id)
#     # print(request.user.subscription_id)
#     subscriptions = Subscription.objects.all()

#     if isinstance(request.user, AnonymousUser):        
#         context = {
#             'subscriptions': subscriptions,
#         }
#     else:  # Remove the unnecessary colon after elif
#         try:
#             currPayment = Payment.objects.get(id=request.user.subscription_id)

#             if currPayment.canceled:
#                 context = {
#                     'subscriptions': subscriptions,
#                     'currSubscription': 'FREE',
#                     'guest': 'free',
#                 }

#             else:
#                 currSubscription = Subscription.objects.get(id=currPayment.subscription_object_id).title
#                 # print('payment')
#                 # print(currSubscription)

#                 context = {
#                     'subscriptions': subscriptions,
#                     'currSubscription': currSubscription,
#                 }    
#         except Payment.DoesNotExist:
#             context = {
#                 'subscriptions': subscriptions,
#                 'currSubscription': 'FREE',
#             }

            


#     return render(request, 'base.html',context=context)

# def testdall(request):
#     return render(request, 'testdall.html')


# def testdallreq(request):
#     if request.method == 'POST':
#         data = json.loads(request.body.decode('utf-8'))
#         user_input = data.get('user_input', '')
#         genImg = dall_e(user_input)

#         request.user.generated_Images.append(genImg)

#         request.user.save()

#         return JsonResponse({'response': f"{genImg}"})


from django.http import HttpResponse
from PIL import Image
from io import BytesIO
from django.shortcuts import render

def lower_resolution_image(request, image_path):
    # Construct the full path to the original image
    original_image_path = f"static/assets/dallegenerated/img/{image_path}"
    
    
    # Load the original image
    original_image = Image.open(original_image_path)

    # Set the desired lower resolution (e.g., 50% of original dimensions)
    lower_resolution = (original_image.width // 2, original_image.height // 2)

    # Resize the image to the lower resolution
    resized_image = original_image.resize(lower_resolution, Image.ANTIALIAS)

    # Save the resized image to a BytesIO buffer
    output_buffer = BytesIO()
    resized_image.save(output_buffer, format='JPEG')
    image_data = output_buffer.getvalue()

    # Set the appropriate content type for the response
    response = HttpResponse(content_type='image/jpeg')

    # Write the image data to the response
    response.write(image_data)

    return response

def mid_resolution_image(request, image_path):
    # Construct the full path to the original image
    original_image_path = f"static/assets/dallegenerated/img/{image_path}"
    
    
    # Load the original image
    original_image = Image.open(original_image_path)

    # Set the desired lower resolution (e.g., 50% of original dimensions)
    lower_resolution = (int(original_image.width * 0.8), int(original_image.height * 0.8))

    # Resize the image to the lower resolution
    resized_image = original_image.resize(lower_resolution, Image.ANTIALIAS)

    # Save the resized image to a BytesIO buffer
    output_buffer = BytesIO()
    resized_image.save(output_buffer, format='JPEG')
    image_data = output_buffer.getvalue()

    # Set the appropriate content type for the response
    response = HttpResponse(content_type='image/jpeg')

    # Write the image data to the response
    response.write(image_data)

    return response





def saveImg(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        imgs = data.get('imgs', '')
        type = data.get('type', '')

        if type == 'image':
            request.user.generated_Images += imgs
            request.user.image_gen_count += 1
            request.user.save()
            return JsonResponse({'response': 'ok'})

        if type == 'logo':    
            request.user.generated_Images_Logo += imgs
            request.user.logo_gen_count += 1
            request.user.save()
            return JsonResponse({'response': 'ok'})


def template_1(request):
    return render(request, 'templates/template_1.html')

def test_text(request):
    return render(request, 'templates/test.txt')

def template_2(request):
    return render(request, 'templates/template_2.html')

def template_3(request):
    return render(request, 'templates/template_3.html')

@csrf_exempt
def contact_us_form_handler(request):
    data = json.loads(request.body)
    send_mail(
        "LandlyAI contact us form submission",
        f"""
        Name: {data['full-name']}
        Email: {data['email']}
        Phone: {data['number']}
        Subject: {data['subject']}
        Message: {data['message']}
        """,
        settings.EMAIL_FROM,
        ['landlyai.sro@gmail.com']
    )
    return JsonResponse({'ok': True, 'message': 'Form successfully submitted'})


def subscription_form_handler(request):
    data = json.loads(request.body)
    email = data['email']

    send_mail(
        "LandlyAI early bird request submitted",
        f"""
        Hello,

        We have received your LandlyAI early bird request.

        We are launching something super cool. We shall be back with our website's updated version soon.

        --
        Best Regards
        Team LandlyAI
        """,
        settings.EMAIL_FROM,
        [email],
        ['landlyai.sro@gmail.com']
    )

    nwdt = subscriberList(email=email)
    nwdt.save()

    return JsonResponse({'ok': True, 'message': 'Form successfully submitted','email': email})
    
    

def my_custom_page_not_found_view(request, exception):
    return render(request, '404.html', status=404)