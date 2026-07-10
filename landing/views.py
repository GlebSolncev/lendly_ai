from django.http import JsonResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404
import ast
import random
import string
import subprocess
import pprint
from payments.models import Subscription, Payment
from landing.chatgpt_service import chat_gpt_service
from landing.models import Landing, Template, Part, LandingImage, Pages
from django.forms.models import model_to_dict
from landing.midjourney_service import midjourney_service
from landing.newGptService import newGptService
from landing.new_midjourney_service import new_midjourney_service
import landing.image_service as image_service
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
import json
from base.dall_e import dall_e  
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser

import os


def editor(request, id):
    
    if not request.user.subscription_id:
        return redirect(reverse('index') + '#pricingSection')

    
    else:
        currPayment = Payment.objects.get(id=request.user.subscription_id)
        if currPayment.canceled:
            return redirect(reverse('index') + '#pricingSection')



    landing = get_object_or_404(Landing, id=id)
    request.user.chosen_landing = landing
    request.user.save()

    if request.user.subscription_id:
        currPayment = Payment.objects.get(id=request.user.subscription_id)
        currSubscription = Subscription.objects.get(id=currPayment.subscription_object_id).title
    else:
        currSubscription = 'FREE'
    # chat_gpt_service.generate_landing(landing)
    
    company_name_dict = ast.literal_eval(landing.company_name)


    context = {
        'landing': landing,
        'templates': Template.objects.all(),
        'images': image_service.get_landing_images(landing),
        'projectFresh': company_name_dict['text'],
        'currSubscription' : currSubscription
    }

    return render(request, 'editor.html', context=context)

def default(request):
    return render(request, 'templates/default.html')

def projects(request):

    if not request.user.subscription_id:
        return redirect(reverse('index') + '#pricingSection')
    else:
        currPayment = Payment.objects.get(id=request.user.subscription_id)
        if currPayment.canceled:
            return redirect(reverse('index') + '#pricingSection')


    if request.user.subscription_id:
        currPayment = Payment.objects.get(id=request.user.subscription_id)
        if currPayment.canceled:
            subs = 'free'
            projectAddLimit = getattr(Template.objects.get(id='2'), subs.lower())
        else:
            subs = Subscription.objects.get(id=currPayment.subscription_object_id).title
            projectAddLimit = getattr(Template.objects.get(id='2'), subs.lower())

    else:
        subs = 'free'
        projectAddLimit = getattr(Template.objects.get(id='2'), subs.lower())


    projectCount = request.user.projectsCount
    context = {
        'projectCount': projectCount,
        'projectAddLimit': projectAddLimit,
    }
    return render(request, 'projects.html',context)


def project_add(request):
    if request.method != 'POST':
        return redirect('projects')


    if request.user.subscription_id:
        currPayment = Payment.objects.get(id=request.user.subscription_id)
        if currPayment.canceled:
            subs = 'free'
            projectAddLimit = getattr(Template.objects.get(id='2'), subs.lower())
        else:
            subs = Subscription.objects.get(id=currPayment.subscription_object_id).title
            projectAddLimit = getattr(Template.objects.get(id='2'), subs.lower())

    else:
        subs = 'free'
        projectAddLimit = getattr(Template.objects.get(id='2'), subs.lower())


    projectCount = request.user.projectsCount



    
    if projectCount < projectAddLimit:
        landing = Landing(
            user=request.user,
            template=Template.objects.get(template="template_1.html"),
            title=request.POST.get('title'))
        request.user.projectsCount += 1
        request.user.save()
        landing.save()
       
        return redirect('editor', id=landing.id)
    
    else:

        return redirect('projects')

    


def view(request, id):
    landing = get_object_or_404(Landing, id=id)
    images = image_service.get_landing_images(landing)
    return render(request, f'templates/{landing.template.template}', context={'landing': landing, 'images': images})


def change(request, id):
    landing = get_object_or_404(Landing, id=id)
    if request.method != 'POST':
        return redirect('editor', id=landing.id)

    field = request.POST.get('field')
    part = Part.objects.get(slug=field)

    index = int(request.POST.get('index'))
    value = request.POST.get('value')
    try:
        truValue = ast.literal_eval(request.POST.get('value'))
    except ValueError as e:
        print(f"Error: {e}")

    if not field:
        return redirect('editor', id=landing.id)

    # if part.slug == 'product_title' or part.slug == 'product_price':
    #     landing.__setattr__(field, value)
    #     landing.__setattr__(field + '_list', value)
    #     landing.save()
    #     save_landing(request, landing)
    #     return JsonResponse({'status': True})

    if part.type == 'single':
        field_value = getattr(landing, field + '_list')
        values = ast.literal_eval(field_value)
        print(type(values))



        if value:
            field_value = ast.literal_eval(getattr(landing, field))

            if field_value == values[index]:
                values[index] = truValue
                landing.__setattr__(field, truValue)
            else:
                values[index] = truValue

        if not value:
            landing.__setattr__(field, values[index])
        landing.__setattr__(field + '_list', values)
    else:
        
        field_value_list = getattr(landing, field + '_list')
        values_list = ast.literal_eval(field_value_list)
      
        field_value = getattr(landing, field)
        values = ast.literal_eval(field_value)


        if value:
            if values_list[index] in values:
                values.remove(values_list[index])
            values_list[index] = truValue



       
        if values_list[index] not in values or not truValue:
            values.append(values_list[index])


      
        
        landing.__setattr__(field, values )
        landing.__setattr__(field + '_list', values_list)
        
     
    landing.save()
    save_landing(request, landing)


    return JsonResponse({'status': True})


def remove(request, id):
    landing = get_object_or_404(Landing, id=id)
    if request.method != 'POST':
        return redirect('editor', id=landing.id)

    field = request.POST.get('field')
    part = Part.objects.get(slug=field)
    if part.type != 'multiple':
        return redirect('editor', id=landing.id)

    value = ast.literal_eval(request.POST.get('value'))

    if not field:
        return redirect('editor', id=landing.id)

    field_value = getattr(landing, field)
    values = ast.literal_eval(field_value)
    values.remove(value)

    print(values)
    print(value)

    if not values:
        values = []
    landing.__setattr__(field, values)
    landing.save()

    save_landing(request, landing)

    return JsonResponse({'status': True})


def generate(request, id):
    landing = get_object_or_404(Landing, id=id)



    if ast.literal_eval(landing.company_name).get("randomStr", "").lower().replace(' ', ''):
        random_string = ast.literal_eval(landing.company_name).get("randomStr", "").lower().replace(' ', '')
    else:
        random_string = ''.join(random.choices(string.ascii_lowercase, k=5))


   
    landing.company_name = f'{{"id":"1cn","text": "{request.POST.get("company_name")}","randomStr":"{random_string}"}}'
    landing.company_description = request.POST.get('company_description')
    # landing.template = Template.objects.get(template="template_1.html")
    # landing.template = Template.objects.get(template=request.POST.get('template'))



    # landing.text_only = bool(int(request.POST.get('text_only')))
    landing.save()

    chat_gpt_service.generate_landing(landing)

    save_landing(request, landing)
   

    return JsonResponse({'status': True})


def generate_more(request, id):
    landing = get_object_or_404(Landing, id=id)
    field = request.POST.get('field')

    texts, value = chat_gpt_service.generate_landing(landing, fields=[field])
    part = Part.objects.get(slug=field)
    return JsonResponse({'status': True, 'texts': texts, 'part': model_to_dict(part), 'value': value})


def delete(request, id):
    landing = get_object_or_404(Landing, id=id)
    landing.delete()
    return redirect('projects')



def save_info(request, id):
    landing = get_object_or_404(Landing, id=id)

    landing.facebook = {'id':'fc','text':request.POST.get('facebook')} 
    landing.youtube = {'id':'yt','text':request.POST.get('youtube')}  
    landing.instagram = {'id':'in','text':request.POST.get('instagram')} 
    landing.twitter =  {'id':'tw','text':request.POST.get('twitter')}  

    landing.phone =  {'id':'ph','text':request.POST.get('phone')} 
    landing.email = {'id':'em','text':request.POST.get('email')} 
    landing.address = {'id':'ad','text':request.POST.get('address')}
    landing.map =  {'id':'ph','text':request.POST.get('map')} 

    landing.save()

    save_landing(request, landing)

    return JsonResponse({'status': True})



def updateColor(request, id):
    if request.method == 'POST':
        landing = get_object_or_404(Landing, id=id)

        data = json.loads(request.body.decode('utf-8'))
        newVal = data.get('newVal', '')
        field = data.get('field', '')
        type = data.get('type', '')
    
        currentVal = getattr(landing, field, {})

        currentVal[type] = newVal

        setattr(landing, field, currentVal)
        landing.save()  


        return JsonResponse({'status': True})




def updateData(request, id):
    if request.method == 'POST':
        landing = get_object_or_404(Landing, id=id)
        data = json.loads(request.body.decode('utf-8'))
        dataVal = data.get('data', '')
        newVal = data.get('newValue', '')
        print(dataVal,newVal)
        # breakpoint()

        landing.__setattr__(dataVal, newVal)
        landing.save()  

        return JsonResponse({'status': True})

def active_elements(request, id):
    if request.method == 'POST':
        landing = get_object_or_404(Landing, id=id)
        data = json.loads(request.body.decode('utf-8'))
        field = data.get('field', '')

        if field in landing.active_elements:
            # If 'hero' is already present, remove it
            landing.active_elements.remove(field)
        else:
            # If 'hero' is not present, append it
            landing.active_elements.append(field)
        landing.save()

        return JsonResponse({'status': True})


def view_site(request, id):
    landing = get_object_or_404(Landing, id=id)
    save_landing(request, landing)
    return redirect('https://' + landing.get_domain())
    
def publish(request, id):
    landing = get_object_or_404(Landing, id=id)

    if request.method == 'POST':
        landing.domain = request.POST.get('domain')
        landing.save()
        return redirect('https://' + landing.get_domain())

    save_landing(request, landing)

    context = {
        'landing': landing,
    }
    return render(request, 'publish.html', context=context)


def updateMeta(request,id):
    landing = get_object_or_404(Landing, id=id)

    data = json.loads(request.body.decode('utf-8'))
    mdata = data.get('data', '')


    
    landing.meta = mdata
    landing.save()

    save_landing(request, landing)

    return JsonResponse({'ok': True})







def genMeta(request,id):
    landing = get_object_or_404(Landing, id=id)

    import openai
    from django.conf import settings


    data = json.loads(request.body.decode('utf-8'))
    getprompt = data.get('prompt', '')
    print(getprompt)

    openai.api_key = settings.CHAT_GPT_KEY

    response = openai.Completion.create(
        model='gpt-3.5-turbo-instruct',
        prompt= getprompt+', give everything in simple text and with no line breaks and any other segmented data',  
        max_tokens=150
    )    

    data = response.choices[0].text
    data_without_linebreaks = data.replace('\n', '').replace('\r', '').replace('"', '')


    save_landing(request, landing)

    return JsonResponse({'data': data_without_linebreaks})



def altImage(request, id):
    landing = get_object_or_404(Landing, id=id)

    data = json.loads(request.body.decode('utf-8'))
    fieldType = data.get('fieldType', '')
    newVal = data.get('newVal', '')

    try:
        img = LandingImage.objects.get(type=fieldType, landing=landing)
    except LandingImage.DoesNotExist:
        img = None


    if not img:
        img = LandingImage()
        img.landing = landing
        img.type = fieldType
        img.url = '/static/assets/img/placeholder_img.jpg'
    
    img.alt = newVal
    img.save()


    save_landing(request, landing)


    return JsonResponse({'ok': True})



@csrf_exempt
def generate_img(request, id):
    landing = get_object_or_404(Landing, id=id)
    img_type = request.POST.get('type')
    prompt = request.POST.get('description')
    imgUrl = request.POST.get('imgUrl')
    message_id = request.POST.get('message_id')
  
    try:
        img = LandingImage.objects.get(type=img_type, landing=landing)
    except LandingImage.DoesNotExist:
        img = None
    if not img:
        img = LandingImage()
        img.landing = landing
        img.type = img_type

   
    img.description = prompt
    img.file = None

    img.message_id = message_id
    img.save()
    url = imgUrl

    img.url = url
    img.save()

    save_landing(request, landing)

    return JsonResponse({'ok': True})

# neww image gen midjourney code

def new_image_gen(request,id):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        description = data.get('description', '') 

        if description =='' :
            description = 'random'

        image_response = new_midjourney_service.main(description)
        return JsonResponse({'mId' :image_response['messageId']})

def new_image_gen_periodic(request,id):
    if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            message_id = data.get('message_id', '') 
            completed_image_data = new_midjourney_service.fetch_to_completion(message_id, 0)

            print(completed_image_data)
            if completed_image_data['progress'] != 100:
                return JsonResponse({'image_urls' : completed_image_data['progressImageUrl'],'buttonMessageId' : '', 'progress': completed_image_data["progress"] })
            else:
                return JsonResponse({'image_urls' : completed_image_data['response']['imageUrls'][3],'buttonMessageId' :  completed_image_data['response']['buttonMessageId'], 'progress': completed_image_data["progress"]})
        # return JsonResponse({'completed_image_data' : completed_image_data })

@csrf_exempt
def upload_img(request, id):
    landing = get_object_or_404(Landing, id=id)
    type_img = request.POST.get('type')
    image = request.FILES.get('image')
    if not image:
        raise Exception('no img')
    try:
        img = LandingImage.objects.get(landing=landing, type=type_img)
    except LandingImage.DoesNotExist:
        img = LandingImage()
        img.landing = landing
        img.type = type_img
    img.url = None
    img.message_id = None
    img.description = ""
    img.file = request.FILES.get('image')
    img.save()

    save_landing(request, landing)

    return redirect('editor', id=landing.id)


@csrf_exempt
def template_1_email_handler(request, id):
    landing = get_object_or_404(Landing, id=id)
    data = json.loads(request.body)
    send_mail(
        f"{landing.company_name} form submission",
        f"""
        Name: {data['full-name']}
        Email: {data['email']}
        Phone: {data['number']}
        Subject: {data['subject']}
        Message: {data['message']}
        """,
        settings.EMAIL_FROM,
        landing.email_receivers
    )
    return JsonResponse({'ok': True, 'message': 'Form successfully submitted'})


@csrf_exempt
def template_2_email_handler(request, id):
    landing = get_object_or_404(Landing, id=id)
    send_mail(
        f"{landing.company_name} form submission",
        f"""
        Name: {request.POST.get('name', None)}
        Email: {request.POST.get('email', None)}
        Subject: {request.POST.get('subject', None)}
        Message: {request.POST.get('message', None)}
        """,
        settings.EMAIL_FROM,
        landing.email_receivers
    )
    return JsonResponse({'ok': True})


@csrf_exempt
def template_4_email_handler(request, id):
    landing = get_object_or_404(Landing, id=id)
    send_mail(
        f"{landing.company_name} form submission",
        f"""
        Name: {request.POST.get('userName', None)}
        Email: {request.POST.get('userEmail', None)}
        Phone: {request.POST.get('userPhone', None)}
        Message: {request.POST.get('userMessage', None)}
        """,
        settings.EMAIL_FROM,
        landing.email_receivers
    )
    return JsonResponse({'ok': True})


def save_landing(request, landing):

    if request.user.subscription_id:
        currPayment = Payment.objects.get(id=request.user.subscription_id)
        currSubscription = Subscription.objects.get(id=currPayment.subscription_object_id).title
    else:
        currSubscription = 'FREE'


    if not (currSubscription == 'FREE' or currSubscription == 'STARTER'):
        
        content = view(request, landing.id).content.decode("utf-8")
        f = open(f"landing/landings/{landing.get_domain()}.html", "w")
    
        f.write(content)
        f.close()
        breakpoint()
        nginx_config = f'/etc/nginx/custom-subdomain/{landing.get_domain()}.conf'
        if os.path.isfile(nginx_config):
            return
        with open('landing/templates/nginx_config.txt') as f:
            content_nginx = f.read()
            content_nginx = content_nginx.replace('DOMAIN', landing.get_domain())
            content_nginx = content_nginx.replace('ROOT', '/var/www/landing_ai/landing/landings')
            content_nginx = content_nginx.replace('FILENAME', f'{landing.get_domain()}.html')


        f = open(nginx_config, 'w')
        f.write(content_nginx)
        f.close()

        os.system(f'certbot --nginx -d {landing.get_domain()} --non-interactive --redirect')
        os.system('systemctl restart nginx')
    




# new app

@login_required
def getStarted(request):

    if not request.user.subscription_id:
        return redirect(reverse('index') + '#pricingSection')


    pages_count = Pages.objects.filter(user_id=request.user.id).count()

    
    try:
        currPayment = Payment.objects.get(id=request.user.subscription_id)

        if currPayment.canceled:

            if not pages_count < 1:
                return redirect('allProjects')

        else:
            pageLimit = Subscription.objects.get(id=currPayment.subscription_object_id).web_page_limit
          
            if not pages_count < pageLimit:
                return redirect('allProjects')
            
    except Payment.DoesNotExist:

        if not pages_count < 1:
            return redirect('allProjects')

  
    return render(request,'getStarted.html')

@login_required
def create(request,id):

    if not request.user.subscription_id:
        return redirect(reverse('index') + '#pricingSection')
        

    page = get_object_or_404(Pages, id=id)


    context = {
        'page':page,
    }
    return render(request,'create.html', context=context)

@login_required
def themePicker(request,id):

        
    if not request.user.subscription_id:
        return redirect(reverse('index') + '#pricingSection')

    page = get_object_or_404(Pages, id=id)

    context = {
        'page':page
    }
    return render(request,'themePicker.html', context=context)

def createPage(request):


    if not request.user.subscription_id:
        return redirect(reverse('index') + '#pricingSection')

    if request.method == 'POST':


        pages_count = Pages.objects.filter(user_id=request.user.id).count()
        try:
            currPayment = Payment.objects.get(id=request.user.subscription_id)

            if currPayment.canceled:

                if not pages_count < 1:
                    
                    return JsonResponse({'status':'no'})

            else:
                pageLimit = Subscription.objects.get(id=currPayment.subscription_object_id).web_page_limit
            
                if not pages_count < pageLimit:
                    
                    return JsonResponse({'status':'no'})
            
        except Payment.DoesNotExist:

            if not pages_count < 1:
                
                return JsonResponse({'status':'no'})

        data = json.loads(request.body.decode('utf-8'))    
        desc = data.get('description', '')
        sections = data.get('sections', '')
        language = data.get('language', '')
        section_headings = createSections(desc,sections)
        pages = Pages(
            user=request.user,
            desc=desc,
            sections=sections,
            language = language,
            sectionHeadings = section_headings,  
            randomString = ''.join(random.choices(string.ascii_lowercase, k=5))
        )   
        pages.save()        
        return JsonResponse({'status':'ok','pId' : pages.id})
    


def addMoreDetails(request,id):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        page = get_object_or_404(Pages, id=id)

        textAmt = data.get('textAmt', '')
        imageType = data.get('imageType', '')
        imageStyle = data.get('imageStyle', '')


        page.imageStyle=imageStyle
        page.imageType = imageType
        page.textAmt = textAmt  
        
        page.save()


    return JsonResponse({
        'status':'ok',
    })  

def updateSecHeadOrder(request,id):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        page = get_object_or_404(Pages, id=id)

        sectionHeadings = data.get('sectionHeadings', '')

        page.sectionHeadings=sectionHeadings
   
        page.save()


    return JsonResponse({
        'status':'ok',
    })  

def updateTheme(request,id):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        page = get_object_or_404(Pages, id=id)

        themeId = data.get('themeId', '')

        page.themeId=themeId
   
        page.save()


    return JsonResponse({
        'status':'ok',
    })  





def reGenPage(request,id):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        page = get_object_or_404(Pages, id=id)

        desc = data.get('description', '')
        sections = data.get('sections', '')
        language = data.get('language', '')

        section_headings = createSections(desc,sections)

        page.desc=desc
        page.sections=sections
        page.language = language
        page.sectionHeadings = section_headings  
        
        page.save()

        return JsonResponse({
            'status':'ok',
            "newSecHeading":section_headings,            
        })

# def createSections(desc,sections):
#     char = 15
#     extraText = 'and dont include seperate texts just a simple single line statement'
#     section_prompts = [
#         {
#             heading : 'hero',
#             prompt : f"Give me an Intro section title in {char} characters related to '{desc}' {extraText}",
#         }
        
#         f"Give a title for About Us section in {char} characters for '{desc}' {extraText}",
#         f"Give a title for Services section in {char} characters for '{desc}' {extraText}",
#         f"Give a title for a Team section in {char} characters for '{desc}' {extraText}",
#         f"Give a title for gallery section in {char} characters for '{desc}' {extraText}",
#         f"Give a title for FAQ section in {char} characters for '{desc}' {extraText}",
#         f"Give a title for stats section in {char} characters for '{desc}' {extraText}",
#         f"Give a title for Testimonials section in {char} characters for '{desc}' {extraText}",
#         f"Give a title for Press section in {char} characters for '{desc}' {extraText}",
#     ]

#     section_headings = []

#     for prompt in section_prompts:
#         if len(section_headings) >= int(sections):
#             break
#         heading = newGptService.sendPrompt(prompt, 40)

#         section_headings.append({ 'content':heading})

#     return section_headings
  


def createSections(desc, sections):
    extraText = 'make it according to the section type and also make it unique and dont repeat, give in 4 words no more than that'
    
    section_prompts = [
        {
            'heading': 'hero',
            'prompt': f"Give me an Intro section title characters related to '{desc}' {extraText}",
        },
        {
            'heading': 'about',
            'prompt': f"Give a title for About Us section characters for '{desc}' {extraText}",
        },
        {
            'heading': 'service',
            'prompt': f"Give a title for Services section characters for '{desc}' {extraText}",
        },
        {
            'heading': 'team',
            'prompt': f"Give a title for a Team section characters for '{desc}' {extraText}",
        },
        {
            'heading': 'gallery',
            'prompt': f"Give a title for gallery section characters for '{desc}' {extraText}",
        },
        {
            'heading': 'faq',
            'prompt': f"Give a title for FAQ section characters for '{desc}' {extraText}",
        },
        {
            'heading': 'stats',
            'prompt': f"Give a title for stats section characters for '{desc}' {extraText}",
        },
        {
            'heading': 'testimonial',
            'prompt': f"Give a title for Testimonials section characters for '{desc}' {extraText}",
        },
        {
            'heading': 'press',
            'prompt': f"Give a title for Press section characters for '{desc}' {extraText}",
        },
        {
            'heading': 'contact form',
            'prompt': f"give an alternate section name to 'contact us' in less that 3 words and just a single phrase",
        },
    ]

    section_headings = []

    # Assuming newGptService.sendPrompt is a function that takes a prompt and returns a response
    for prompt_dict in section_prompts:
        if len(section_headings) >= int(sections):
            break
        # Assuming newGptService.sendPrompt returns the response as a string
        response = newGptService.sendPrompt(prompt_dict['prompt'], 40)

        # Append the heading and response as a dictionary to the section_headings list
        section_headings.append({'head': prompt_dict['heading'], 'response': response})

    return section_headings










def promptGet(request,id):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        # page = get_object_or_404(Pages, id=id)

        prompt = data.get('prompt', '')
        maxT = data.get('maxT', '')

        res = newGptService.sendPrompt(prompt, maxT)
        return JsonResponse({
            'status':'ok',
            "res":res,            
        })

@login_required
def edit(request,id):


    if not request.user.subscription_id:
        return redirect(reverse('index') + '#pricingSection')

    subscriptions = Subscription.objects.all()

    page = get_object_or_404(Pages, id=id)

    print(page.get_domain_new())

    savePageNew(request, page)

    try:
        currPayment = Payment.objects.get(id=request.user.subscription_id)

        if currPayment.canceled:
            context = {
                'page':page,

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
                'page':page,

                'subscriptions': subscriptions,
                'currSubscription': currSubscription,
                'currSubscriptionClass': currSubscriptionClass,
            }    
    except Payment.DoesNotExist:
        context = {
            'page':page,

            'subscriptions': subscriptions,
            'currSubscription': 'FREE',
            'currSubscriptionClass': 'free',
        }


    return render(request,'edit.html', context=context)


@login_required
def preview(request,id):

    if not request.user.subscription_id:
        return redirect(reverse('index') + '#pricingSection')
    
    page = get_object_or_404(Pages, id=id)

    context = {
        'page':page
    }
    return render(request,'preview.html', context=context)

@login_required
def respPreview(request,id):


    if not request.user.subscription_id:
        return redirect(reverse('index') + '#pricingSection')
    
    page = get_object_or_404(Pages, id=id)

    context = {
        'page':page
    }
    return render(request,'respPreview.html', context=context)

@login_required
def allProjects(request):



    if not request.user.subscription_id:
        return redirect(reverse('index') + '#pricingSection')

    subscriptions = Subscription.objects.all()

    pages = Pages.objects.filter(user_id=request.user.id)
    pages_count = Pages.objects.filter(user_id=request.user.id).count()
    pages_data = []

    for page in pages:
        pages_data.append({
            'desc': page.desc,
            'pid': page.id,
        })



    
    try:
        currPayment = Payment.objects.get(id=request.user.subscription_id)

        if currPayment.canceled:
            context = {
                'pages_data':pages_data,
                'subscriptions': subscriptions,
                'currSubscription': 'FREE',
                'guest': 'FREE',
                'currSubscriptionClass': 'free',
                'pageLimit':1,
                'projectCount': pages_count

            }

        else:
            currSubscription = Subscription.objects.get(id=currPayment.subscription_object_id).title
            currSubscriptionClass = Subscription.objects.get(id=currPayment.subscription_object_id).classname
            pageLimit = Subscription.objects.get(id=currPayment.subscription_object_id).web_page_limit
            # print('payment')
            # print(currSubscription)

            context = {
                'pages_data':pages_data,
                'subscriptions': subscriptions,
                'currSubscription': currSubscription,
                'currSubscriptionClass': currSubscriptionClass,
                'pageLimit':pageLimit,
                'projectCount': pages_count


            }    
    except Payment.DoesNotExist:
        context = {
            'pages_data':pages_data,
            'subscriptions': subscriptions,
            'currSubscription': 'FREE',
            'currSubscriptionClass': 'free',
            'pageLimit':1,
            'projectCount':pages_count

        }


    
    return render(request,'allProjects.html', context=context)

def saveAllPageData(request,id):
    if request.method == 'POST':
        page = get_object_or_404(Pages, id=id)
        data = json.loads(request.body.decode('utf-8'))
        formData = data.get('data', '')

        page.allPageData = formData
        page.save()

        return JsonResponse({
            'status':'ok',
            'res':formData
        })
    

def updateIsFirst(request,id):
    if request.method == 'POST':
        page = get_object_or_404(Pages, id=id)
        data = json.loads(request.body.decode('utf-8'))
        formData = data.get('data', '')

        page.isFirst = formData
        page.save()

        
      

        return JsonResponse({
            'status':'ok',
            'res':formData
        })
    
def updateFavicon(request,id):
    if request.method == 'POST':
        page = get_object_or_404(Pages, id=id)
        data = json.loads(request.body.decode('utf-8'))
        formData = data.get('data', '')
        mtitle = data.get('mtitle', '')
        mKeywords = data.get('mKeywords', '')
        mDescription = data.get('mDescription', '')

        page.favicon = formData
        page.metaTitle = mtitle
        page.metaKeywords = mKeywords
        page.metaDescription = mDescription
     
        
        page.save()

        
      

        return JsonResponse({
            'status':'ok',
            'res':formData
        })
    

import uuid

def upload_image_new(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
    
        unique_filename = str(uuid.uuid4()) + '_' + image.name



        # Define the path where you want to save the image in the static folder
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        
        # Create the directory if it doesn't exist
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # Save the image to the defined directory
        image_path = os.path.join(upload_dir, unique_filename)
        with open(image_path, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)
        
        image_url = os.path.join(settings.MEDIA_URL, 'uploads', unique_filename)
        image_url = image_url.replace('\\', '/')
        return JsonResponse({'url': image_url})
    
    return JsonResponse({'error': 'No image uploaded'}, status=400)
    

def generate_new(request):

    if request.method == 'POST':
        user_input = request.POST.get('genInput')
        

        current_user = request.user
        count = current_user.image_gen_count

        try:   
            currPayment = Payment.objects.get(id = current_user.subscription_id)
    
            if currPayment.canceled:
                
                if count < 12:

                    genImg = dall_e(user_input)
                    request.user.image_gen_count += 1
                    request.user.save()
                    

                    return JsonResponse({'customText': 'ok','imgUrl': genImg})

                else: 
                    return JsonResponse({'customText': 'Limit Reached'})


            else:
            
                # currSubscription = Subscription.objects.get(id=currPayment.subscription_object_id).title
                limit = Subscription.objects.get(id=currPayment.subscription_object_id).image_gen_limit
    

                if count < limit:

                    genImg = dall_e(user_input)
                    request.user.image_gen_count += 1
                    request.user.save()

            
                    return JsonResponse({'customText': 'ok','imgUrl': genImg})

                else: 
                    return JsonResponse({'customText': 'Limit Reached'})

                

        except Payment.DoesNotExist:
         
            if count < 12:

                genImg = dall_e(user_input)
                request.user.image_gen_count += 1
                request.user.save()


                return JsonResponse({'customText': 'ok','imgUrl': genImg})
            else: 
                 
                return JsonResponse({'customText': 'Limit Reached'})






    # return JsonResponse({'url': genImg})


# def publish(request, id):
#     landing = get_object_or_404(Landing, id=id)

#     if request.method == 'POST':
#         landing.domain = request.POST.get('domain')
#         landing.save()
#         return redirect('https://' + landing.get_domain())

#     save_landing(request, landing)

#     context = {
#         'landing': landing,
#     }
#     return render(request, 'publish.html', context=context)


@login_required
def handlePublish(request,id):



    if not request.user.subscription_id:
        return redirect(reverse('index') + '#pricingSection')


    if request.method == 'POST':
        
        page = get_object_or_404(Pages, id=id)
        domain = request.POST.get('domain')
        customdomain = request.POST.get('customdomain').replace(' ', "")
        domain = domain.replace(' ', "-")


        page.domain = f'{domain}-{page.randomString}.landlyai.com'




        try:
            currPayment = Payment.objects.get(id=request.user.subscription_id)

            if currPayment.canceled:
                currSubscriptionClass = 'free'

            else:
                currSubscriptionClass = Subscription.objects.get(id=currPayment.subscription_object_id).classname
                
        except Payment.DoesNotExist:
            currSubscriptionClass = 'free',


        if currSubscriptionClass == 'ai-web-generator':
            page.customDomain = customdomain
        else: 
            page.customDomain = ''

        page.save()

        savePageNew(request, page)
        
        
        return redirect('https://' + page.get_domain_new())

        # return JsonResponse({'url': 'https://' + page.get_domain_new()})

@login_required
def newDelete(request, id):


    if not request.user.subscription_id:
        return redirect(reverse('index') + '#pricingSection')

    page = get_object_or_404(Pages, id=id)
    page.delete()
    return redirect('allProjects')


from django.core.mail import EmailMessage
from django.http import JsonResponse

@csrf_exempt
def send_email_view(request):
    if request.method == 'POST':
        
        # Parse request data
        data = json.loads(request.body)
        body = data.get('body', '')
        recipient = data.get('recipient')

        if not recipient:
            return JsonResponse({'error': 'Recipient email not provided.'})


        try:
            send_mail(
                "You've got a mail",
                body,
                settings.EMAIL_HOST_USER,
                [recipient],
                fail_silently=False,
            )
            return JsonResponse({'message': 'Email sent successfully!'})
        except Exception as e:
            return JsonResponse({'message': 'Error sending email'})

    return JsonResponse({'error': 'Invalid request method.'})


def savePageNew(request, landing):
    subscriptions = Subscription.objects.all()

    try:
        currPayment = Payment.objects.get(id=request.user.subscription_id)
        if currPayment.canceled:
            currSubscriptionClass = 'free'
        else:
            currSubscriptionClass = Subscription.objects.get(id=currPayment.subscription_object_id).classname
    except Payment.DoesNotExist:
        currSubscriptionClass = 'free'  # Убрали лишнюю запятую

    if not currSubscriptionClass == 'ai-tools':
        print('done')

        content = preview(request, landing.id).content.decode("utf-8")

        domain_new = landing.get_domain_new()

        # 1. Исправляем путь к HTML-файлу лендинга через BASE_DIR
        html_file_path = settings.BASE_DIR / 'landing' / 'landings' / f"{domain_new}.html"

        # Автоматически создаем папки landing/landings/, если их вдруг нет
        html_file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(html_file_path, "w", encoding="utf-8") as f:
            f.write(content)

        nginx_config = f'/etc/nginx/custom-subdomain/{domain_new}.conf'
        if os.path.isfile(nginx_config):
            return

        # 2. Исправляем путь к шаблону nginx конфигурации
        nginx_template_path = settings.BASE_DIR / 'landing' / 'templates' / 'nginx_config.txt'

        with open(nginx_template_path, 'r', encoding='utf-8') as f:
            content_nginx = f.read()

        content_nginx = content_nginx.replace('DOMAIN', domain_new)

        # Подставляем правильный абсолютный путь к папке с лендингами для Nginx
        landings_dir = settings.BASE_DIR / 'landing' / 'landings'
        content_nginx = content_nginx.replace('ROOT', str(landings_dir))
        content_nginx = content_nginx.replace('FILENAME', f'{domain_new}.html')

        # 3. Запись конфигурации Nginx
        with open(nginx_config, 'w', encoding='utf-8') as f:
            f.write(content_nginx)

        # 4. Безопасный вызов системных команд (защита от внедрения команд)
        subprocess.run(['certbot', '--nginx', '-d', domain_new, '--non-interactive', '--redirect'], check=True)
        subprocess.run(['systemctl', 'restart', 'nginx'], check=True)