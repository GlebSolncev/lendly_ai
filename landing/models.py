import random
import uuid
import ast
from django.db import models
import json

class Pages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('user.User', verbose_name='Пользователь', on_delete=models.CASCADE, related_name='pages')
    sections = models.CharField('Sections', max_length=300, default='')
    desc = models.CharField('Description', max_length=300, default='')
    randomString = models.CharField('random string', max_length=300, default='')
    language = models.CharField('language', max_length=300, default='')
    sectionHeadings = models.JSONField(default=list, blank=True)
    textAmt = models.CharField('Text amt', max_length=300, default='')
    imageType = models.CharField('Image type', max_length=300, default='')
    imageStyle = models.CharField('Image Style', max_length=300, default='')
    themeId = models.CharField('themeId', max_length=300, default='-1')
    allPageData = models.JSONField(default=list, blank=True)
    isFirst = models.CharField('isFirst', max_length=300, default='false')
    favicon =  models.CharField('favicon', max_length=300, default='')
    metaTitle =  models.CharField('Meta Title', max_length=300, default='')
    metaKeywords =  models.CharField('Meta Keywords', max_length=300, default='')
    metaDescription =  models.CharField('Meta Description', max_length=300, default='')
    domain =  models.CharField('Domain', max_length=300, default='')
    customDomain =  models.CharField('Custom domain', max_length=300, default='')

    
    # def get_domain(self):
    #     if not self.domain:
    #         return self.get_default_domain()
    #     return self.domain

    def get_domain_new(self):
        if not self.customDomain:
            return self.get_default_domain_new()
        return self.customDomain


    def get_default_domain_new_parts(self):
        if self.domain:
            domain = self.domain.replace(f'-{self.randomString}.landlyai.com', "")
            return {
                'domain': domain,
                'randomStr':self.randomString,
                'url':f'{domain}-{self.randomString}.landlyai.com'
            }
        
        text = self.desc

        # Split the text into words
        words = text.split()

        # Take the first two words
        first_two_words = " ".join(words[:2])

        domain = first_two_words.lower().replace(' ', '-')

        randomStr = self.randomString
        return {
            'domain': domain,
            'randomStr':randomStr,
            'url':f'{domain}-{randomStr}.landlyai.com'
        }

    def get_default_domain_new(self):

        if self.domain:
            return self.domain

        text = self.desc

        # Split the text into words
        words = text.split()

        # Take the first two words
        first_two_words = " ".join(words[:2])

        domain = first_two_words.lower().replace(' ', '-')

        randomStr = self.randomString
        return f'{domain}-{randomStr}.landlyai.com'
    

class Landing(models.Model):
    class Verify(models.TextChoices):
        user = 'youtube', 'Youtube'
        moder = 'twitch', 'Twitch'
        admin = 'verified', 'Проверенный'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey('Template', verbose_name='Шаблон', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', verbose_name='Пользователь', on_delete=models.CASCADE, related_name='landings')

    domain = models.CharField('Домен по умолчанию', default='', blank=True, max_length=100)

    title = models.CharField('Название', max_length=100, default='')
    company_name = models.CharField('Название компании', max_length=100, default="{'id': '', 'text': ''}")
    company_description = models.TextField('Описание компании')

    youtube = models.CharField('Youtube', blank=True, default="{'id': 'yt', 'text': ''}", max_length=255)
    twitter = models.CharField('Twitter', blank=True, default="{'id': 'tw', 'text': ''}", max_length=255)
    instagram = models.CharField('Instagram', blank=True, default="{'id': 'in', 'text': ''}", max_length=255)
    facebook = models.CharField('Facebook', blank=True, default="{'id': 'fc', 'text': ''}", max_length=255)

    phone = models.CharField('Телефон', blank=True,  default="{'id': 'ph', 'text': 'Enter Your Phone Number'}", max_length=100)
    email = models.CharField('Телефон', blank=True,  default="{'id': 'em', 'text': 'Enter Your Email'}", max_length=100)
    address = models.CharField('Адрес', blank=True,  default="{'id': 'ad', 'text': 'Enter Your Address'}", max_length=100)
    map = models.CharField('Map', blank=True,  default="{'id': 'map', 'text': ''}", max_length=1055)


    meta = models.JSONField(default=list, blank=True)

    hero_list = models.TextField('Список Hero', default='')
    hero_long_list = models.TextField('Список Hero long', default='')

    def hero_colors_dict():
        return {"bgColor": "default", "fontColor": "default"}
    
    
    hero_colors = models.JSONField(default=hero_colors_dict, blank=True)
    hero_long_colors = models.JSONField(default=hero_colors_dict, blank=True)
    services_colors = models.JSONField(default=hero_colors_dict, blank=True)
    statistics_colors = models.JSONField(default=hero_colors_dict, blank=True)
    testimonials_colors = models.JSONField(default=hero_colors_dict, blank=True)
    cta_colors = models.JSONField(default=hero_colors_dict, blank=True)
    about_us_colors = models.JSONField(default=hero_colors_dict, blank=True)
    product_title_colors = models.JSONField(default=hero_colors_dict, blank=True)
    desc_colors = models.JSONField(default=hero_colors_dict, blank=True)

    def allColors(self):
        return { 
            'hero' : self.hero_colors ,      
            'hero_long' : self.hero_long_colors ,        
            'services' : self.services_colors ,        
            'statistics' : self.statistics_colors ,        
            'testimonials' : self.testimonials_colors ,        
            'cta' : self.cta_colors ,        
            'about_us' : self.about_us_colors ,        
            'product_title' : self.product_title_colors ,        
            'desc' : self.desc_colors ,        
        }
    
    from django.template.defaulttags import register
    
    @register.filter
    def get_item(dictionary, key):
        return dictionary.get(key)

    services_list = models.TextField('Список Services', default='')
    about_us_list = models.TextField('Список About us', default='')
    statistics_list = models.TextField('Список Statistics', default='')
    testimonials_list = models.TextField('Список Testimonials', default='')
    cta_list = models.TextField('Список CTA', default='')
    cta_long_list = models.TextField('Список CTA long', default='')

    hero = models.CharField('Hero', max_length=500)
    hero_long = models.TextField('Hero long')
    services = models.TextField('Services')
    about_us = models.TextField('About us', default='')
    statistics = models.TextField('Statistics')
    testimonials = models.TextField('Testimonials')
    cta = models.CharField('CTA', max_length=500)
    cta_long = models.TextField('CTA long')

    text_only = models.BooleanField("Text Only", default=True)

    product_title = models.CharField('Product Title', default="{'id': 'ptl2', 'text': 'product 2'}", max_length=255)
    product_title_list = models.CharField("Product Title List", default="[{'id': 'ptl1', 'text': 'Product 1'}, {'id': 'ptl2', 'text': 'product 2'}, {'id': 'ptl3', 'text': 'product 3'}, {'id': 'ptl4', 'text': 'product 4'}, {'id': 'ptl5', 'text': 'product 5'}]", max_length=255)
    product_price = models.CharField('Product Price', default="{'id': 'ppl1', 'text': '10$'}", max_length=255)
    product_price_list = models.CharField('Product Price List', default = "[{'id': 'ppl1', 'text': '10$'}, {'id': 'ppl2', 'text': '20$'}, {'id': 'ppl3', 'text': '30$'}, {'id': 'ppl4', 'text': '40$'}, {'id': 'ppl5', 'text': '50$'}]", max_length=255)
    product_features = models.TextField("Product Features", default="[{'id': 'pfl1', 'text': 'Feature 1'}, {'id': 'pfl2', 'text': 'Feature 2'}, {'id': 'pfl3', 'text': 'Feature 3'}, {'id': 'pfl4', 'text': 'Feature 4'}]")
    product_features_list = models.TextField("Product Features List", default="[{'id': 'pfl1', 'text': 'Feature 1'}, {'id': 'pfl2', 'text': 'Feature 2'}, {'id': 'pfl3', 'text': 'Feature 3'}, {'id': 'pfl4', 'text': 'Feature 4'},{'id': 'pfl5', 'text': 'Feature 5'}]")
    product_link = models.TextField("Product Redirect Link", default="{'id': 'prl', 'text': 'Your link'}")
    product_link_list = models.TextField("Product Redirect Link List", default="[{'id': 'prl', 'text': 'Your link'}]")


    class Type(models.TextChoices):       
        default = 'default', 'default' 
        Helvetica = 'Helvetica, sans-serif', 'Helvetica'
        Arial =   'Arial, sans-serif', 'Arial'
        ArialBlack =  'Arial Black, sans-serif','Arial Black'
        Verdana =   'Verdana, sans-serif', 'Verdana'
        Tahoma = 'Tahoma, sans-serif', 'Tahoma'
        TrebuchetMS =  'Trebuchet MS, sans-serif', 'Trebuchet MS'
        Impact =  'Impact, sans-serif','Impact'
        GillSans =  'Gill Sans, sans-serif','Gill Sans'
        TimesNewRoman =  'Times New Roman, serif','Times New Roman'
        Georgia = 'Georgia, serif','Georgia'
        Palatino = 'Palatino, serif','Palatino'
        Baskerville = 'Baskerville, serif','Baskerville'
        AndaléMono = 'Andalé Mono, monospace','Andalé Mono'
        Courier = 'Courier, monospace','Courier'
        Lucida = 'Lucida, monospace','Lucida'
        Monaco = 'Monaco, monospace', 'Monaco'
        BradleyHand = 'Bradley Hand, cursive','Bradley Hand'
        BrushScriptMT = 'Brush Script MT, cursive','Brush Script MT'
        Luminari = 'Luminari, fantasy','Luminari'
        ComicSansMS = 'Comic Sans MS, cursive','Comic Sans MS'

    PrimaryFont = models.CharField('Primary Font', max_length=27, choices=Type.choices, default=Type.default, blank=True)
    SecondaryFont = models.CharField('Secondary Font', max_length=27, choices=Type.choices, default=Type.default, blank=True)





    def default_active_elements():
        return ['hero', 'hero_long', 'services', 'about_us', 'testimonials', 'cta', 'product', 'statistics']

    active_elements = models.JSONField(default=default_active_elements, blank=True)



    
    def get_domain(self):
        if not self.domain:
            return self.get_default_domain()
        return self.domain

    def get_default_domain(self):
        domain = ast.literal_eval(self.company_name)["text"].lower().replace(' ', '')

        if ast.literal_eval(self.company_name).get("randomStr", "").lower().replace(' ', ''):
            randomStr = ast.literal_eval(self.company_name)["randomStr"].lower().replace(' ', '')
            return f'{domain}-{randomStr}.landlyai.com'
    
        return f'{domain}.landlyai.com'
    


    def get_title(self):
        return self.company_name.split(' ')[0]

    def get_title_second(self):
        if len(self.company_name.split(' ')) > 1:
            return self.company_name.split(' ')[1]
        return ''

    def is_new(self):
        return self.hero == ''

    def to_string(self, values):
        return '|'.join(values)

    def to_list(self, value):
        return value.split('|')


    def get_additional(self):


        additional = {
            'facebook': ast.literal_eval(self.facebook),
            'instagram':ast.literal_eval(self.instagram),
            'twitter':ast.literal_eval(self.twitter),
            'youtube':ast.literal_eval(self.youtube),

            'address':ast.literal_eval(self.address),
            'email':ast.literal_eval(self.email),
            'phone':ast.literal_eval(self.phone),
            'map':ast.literal_eval(self.map),
        }



    

        return additional



    def get_company_name(self):
        # company_data = self.company_name
        
        # text = company_data[0]
        # id = company_data[1]

        # company_data_objects = {'text': text, 'id': id}
        company_data = ast.literal_eval(self.company_name)
        return company_data
    
    def get_only_company_name(self):
        # company_data = self.company_name
        
        # text = company_data[0]
        # id = company_data[1]

        # company_data_objects = {'text': text, 'id': id}

        return ast.literal_eval(self.company_name)

    def get_active_hero(self):

        # hero_data = self.hero.split('|')[0].split('@~')

        # text = hero_data[0]
        # id = hero_data[1]

        # hero_data_objects = {'text': text, 'id': id}

        
        return ast.literal_eval(self.hero)

    def get_hero(self):

        # hero = self.hero_list.split('|')
       
    
        
        # hero_objects = []
        # for service in hero:
        #     text, id = service.split('@~')
        #     hero_objects.append({'text': text, 'id': id, 'complete':service})



        return ast.literal_eval(self.hero_list)

    def get_active_hero_long(self):

        # hero_data_long = self.hero_long.split('|')[0].split('@~')

        # text = hero_data_long[0]
        # id = hero_data_long[1]
        # # print(text)

        # hero_data_objects = {'text': text, 'id': id}

        
        return  ast.literal_eval(self.hero_long)
    
    def get_hero_long(self):



        # hero_long = self.hero_long_list.split('|')

        # # Create a list of objects with 'text' and 'id'
        # hero_objects = []
        # for hero in hero_long:
        #     text, id = hero.split('@~')
        #     hero_objects.append({'text': text, 'id': id, 'complete':hero })

        return ast.literal_eval(self.hero_long_list)
        


    def get_services(self):
        # services = self.services_list.split('|')

        # # Create a list of objects with 'text' and 'id'
        # services_objects = []
        # for service in services:
        #     text, id = service.split('@~')
        #     services_objects.append({'text': text, 'id': id})

        return ast.literal_eval(self.services_list)


    def get_service_objects(self):

        services = []

        for service in ast.literal_eval(self.services):


            data = {
                'title': service['text'].split(':')[0] ,
                'id': service['id'],
                'text': service['text'].split(':')[1] if ':' in service['text'] else service['text'].split(':')[0] ,
            }

            services.append(data)
        
        

        return services

    def get_active_service(self):
        # services = []

        # if not self.services:
        #     return []

        # for service in self.services.split('|'):
        #     if not service:
        #         continue

        #     service_data = service.split('@~')
        #     id = service_data[1]

        #     service_subdata = service_data[0].split(':')

        #     title = service_subdata[0]


        #     if len(service_subdata) > 1:
        #         text = service_subdata[1]
                
        #     else:
        #         text = ''

        #     data = {
        #         'title': title,
        #         'id': id,
        #         'text': text,
        #     }

        #     services.append(data)

            # print(services)
        return self.services

    def get_about_us(self):
        return  ast.literal_eval(self.about_us_list) 


    def get_about_us_objects(self):
        about_us = []

        if not self.about_us:
            return []

        for about in ast.literal_eval(self.about_us):
            if not about:
                continue
            
            service_data = about['text'].split(':')
            title = service_data[0]
            if len(service_data) > 1:
                text = service_data[1]
            else:
                text = ''

            data = {
                'id': about['id'],
                'title': title,
                'text': text,
            }

            about_us.append(data)
        return about_us

    def get_statistics(self):
        return  ast.literal_eval(self.statistics_list) 

    def get_statistics_objects(self):
        statistics = []

        if not self.statistics:
            return []

        for statistic in ast.literal_eval(self.statistics):
            if not statistic:
                continue
            
            service_data = statistic['text'].split(':')
            title = service_data[0]
            if len(service_data) > 1:
                text = service_data[1]
            else:
                text = ''

            data = {
                'id': statistic['id'],
                'title': title,
                'text': text,
            }

            statistics.append(data)
        return statistics

    def get_testimonials(self):
        
        # testimonials = []

        # for testimonial in self.testimonials_list.split('|'):
        #     if not testimonial:
        #         continue
        #     data = {
        #         'text': testimonial.split("@~")[0],
        #         'id': testimonial.split("@~")[1],
        #         'complete':testimonial
        #     } 

            
        #     testimonials.append(data)
        return ast.literal_eval(self.testimonials_list)

    def get_testimonials_objects(self):
        # names = ['Andrew', 'David', 'Sofia', 'John', 'Anton', 'Igor', 'Aleksandr', 'Alex', 'Maria', 'Tania']
        # testimonials = []

        # if not self.testimonials:
        #     return []

        # for testimonial in self.testimonials.split('|'):
        #     if not testimonial:
        #         continue
        #     data = {
        #         'title': random.choice(names),
        #         'text': testimonial.split("@~")[0],
        #         'id': testimonial.split("@~")[1],
        #     } 

            
        #     testimonials.append(data)
        return ast.literal_eval(self.testimonials)



    def get_cta_active(self):
        # cta = self.cta.split('|')
        # data = {
        #     'text': cta[0].split('@~')[0],
        #     'id': cta[0].split('@~')[1],
        # } 

        return ast.literal_eval(self.cta)

    def get_cta(self):
    
        # cta = []

        # for indCta in self.cta_list.split('|'):
        #     if not indCta:
        #         continue
        #     data = {
        #         'text': indCta.split("@~")[0],
        #         'id': indCta.split("@~")[1],
        #         'complete':indCta
        #     } 

        #     cta.append(data)
        # return cta

        return ast.literal_eval(self.cta_list)


    def get_cta_long_active(self):
        # cta = []

    
    
        # for indCta in self.cta_long.split('|'):
        #     if not indCta:
        #         continue
        #     data = {
        #         'text': indCta.split("@~")[0],
        #         'id': indCta.split("@~")[1],
        #         'complete':indCta
        #     } 

        #     cta.append(data)
        return ast.literal_eval(self.cta_long)

    def get_cta_long(self):

        # cta = []

        # for indCta in self.cta_long_list.split('|'):
        #     if not indCta:
        #         continue
        #     data = {
        #         'text': indCta.split("@~")[0],
        #         'id': indCta.split("@~")[1],
        #         'complete':indCta
        #     } 

        #     cta.append(data)
        return ast.literal_eval(self.cta_long_list) 

    # def get_product_features(self):
    #     if not self.product_features:
    #         return []

    #     features = []
    #     for feature in self.product_features.split('|'):
    #         if not feature:
    #             continue

    #         features.append(feature)
    #     return features


    def get_product_title(self):
        return  ast.literal_eval(self.product_title) 

    def get_product_price(self):
        return  ast.literal_eval(self.product_price) 

    def get_product_features(self):
        return  ast.literal_eval(self.product_features) 
    
    def get_product_title_list(self):
        return  ast.literal_eval(self.product_title_list) 

    def get_product_price_list(self):
        return  ast.literal_eval(self.product_price_list) 

    def get_product_features_list(self):
        return  ast.literal_eval(self.product_features_list) 


    def get_product_link(self):
        print(ast.literal_eval(self.product_link))
        return  ast.literal_eval(self.product_link) 
    
    def get_product_link_list(self):
        return  ast.literal_eval(self.product_link_list) 

    @property
    def email_receivers(self):
        receivers = [self.user.email]
        if self.email:
            receivers.append(self.email)
        return receivers

    class Meta:
        verbose_name = 'Лэндинг'
        verbose_name_plural = 'Лэндинги'

    def __str__(self):
        return f'{self.user} {self.company_name}'


class Template(models.Model):
    title = models.CharField('Название', max_length=100)
    template = models.CharField('Шаблон', max_length=100)
    parts = models.ManyToManyField('Part', verbose_name='Части')
    sort = models.IntegerField('Сортировка', default=0)
    example = models.ForeignKey('Landing', verbose_name='Пример', blank=True, on_delete=models.PROTECT, default=None, null=True, related_name='example_templates')

    free = models.IntegerField('Free Limit', default=0, blank=True)
    light = models.IntegerField('Light Limit', default=0, blank=True)

    starter = models.IntegerField('Starter Limit', default=0, blank=True)
    basic = models.IntegerField('Basic Limit', default=0, blank=True)
    pro = models.IntegerField('Pro Limit', default=0, blank=True)

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'
        ordering = ('-sort', '-id',)

    def __str__(self):
        return self.title


class Part(models.Model):
    class Type(models.TextChoices):
        single = 'single', 'Одно значение'
        multiple = 'multiple', 'Много значений'

    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', default='', blank=True)
    type = models.CharField('Тип', max_length=20, choices=Type.choices, default=Type.single, blank=True)
    slug = models.CharField('Slug', max_length=20)
    sort = models.IntegerField('Сортировка', default=0)

    class Meta:
        verbose_name = 'Часть'
        verbose_name_plural = 'Части'
        ordering = ('-sort', '-id',)

    def __str__(self):
        return self.title


class LandingImage(models.Model):
    landing = models.ForeignKey('Landing', on_delete=models.CASCADE)
    file = models.FileField('Landing', null=True, blank=True)
    url = models.CharField('Url', null=True, blank=True, max_length=255)
    message_id = models.CharField('Midjourney Message Id', null=True, blank=True, max_length=255)
    type = models.CharField('Image type', null=True, blank=True, max_length=255)
    description = models.TextField('Image description', null=True, blank=True)
    alt = models.TextField('Image Alt Text', null=True, blank=True)

    @property
    def img_url(self):
        if self.file:
            return self.file.url
        else:
            return self.url

    def __str__(self):
        return self.img_url



