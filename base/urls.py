from django.urls import path
import base.views as base
from . import views

handler404 = "base.views.my_custom_page_not_found_view"

urlpatterns = [
    # path('', base.underConstruction, name='underConstruction'),
    # path('temp-index/', base.index, name='index'),
    path('', base.index, name='index'),
    # path('', base.indexTemp, name='indexTemp'),
    # path('', base.underConstruction, name='underConstruction'),
    path('support/', base.support, name='support'),
    path('about/', base.about, name='about'),
    path('seo_keyword/', base.chat_view, name='seo_keyword'),
    path('content_creator/', base.content_creator, name='content_creator'),
    path('underConstruction/', base.underConstruction, name='underConstruction'),
    path('image_generator/', base.image_generator, name='image_generator'),
    path('logo_generator/', base.logo_generator, name='logo_generator'),
    path('image_generator_periodic/', base.image_generator_periodic, name='image_generator_periodic'),
    path('logo_generator_periodic/', base.logo_generator_periodic, name='logo_generator_periodic'),
    path('page/<slug>/', base.page, name='page'),
    path('template_1/', base.template_1,   name='template_1'),
    path('template_2/', base.template_2, name='template_2'),
    path('template_3/', base.template_3, name='template_3'),
    path('contact-us/', base.contact_us_form_handler, name="contact_us"),
    path('subscription/', base.subscription_form_handler, name="subscription"),

    path('car-dealership/', base.car_dealership, name="car_dealership"),
    path('display-ads/', base.display_ads, name="display_ads"),    
    path('ecommerce-sales/', base.ecommerce_sales, name="ecommerce_sales"),    
    path('education/', base.education, name="education"),   
    path('finance/', base.finance, name="finance"),    
    path('games-and-entertainment/', base.games_and_entertainment, name="games_and_entertainment"),    
    path('health-and-beauty/', base.health_and_beauty, name="health_and_beauty"),   

    path('insurance/', base.insurance, name="insurance"),    
    path('lead-generation/', base.lead_generation, name="lead_generation"),    
    path('marketing-and-advertising/', base.marketing_and_advertising, name="marketing_and_advertising"),    
    path('real-estate/', base.real_estate, name="real_estate"),    
    path('retargeting/', base.retargeting, name="retargeting"),    
    path('search-ads/', base.search_ads, name="search_ads"),    
    path('social-ads/', base.social_ads, name="social_ads"),    
    path('software-and-tech/', base.software_and_tech, name="software_and_tech"),    
    path('sports-and-events/', base.sports_and_events, name="sports_and_events"),    
    path('test-text/', base.test_text, name="test_text"),    
    # path('testdall/', base.testdall, name="testdall"),    
    # path('testdallreq/', base.testdallreq, name="testdallreq"),    
    path('saveImg/', base.saveImg, name="saveImg"),
    path('lower_resolution/<path:image_path>/', views.lower_resolution_image, name='lower_resolution_image'),
    path('mid_resolution_image/<str:image_path>/', base.mid_resolution_image, name='mid_resolution_image'),
    # path('404/', base.my_custom_page_not_found_view, name="my_custom_page_not_found_view"),    
]


