# utils.py

from django.urls import get_resolver, URLPattern, URLResolver

def get_urlpatterns():
    urlpatterns = []
    urlconf_modules = ['base.urls','landing.urls','landing_ai.urls','payments.urls','user.urls']  # Add your app's URL configuration module here

    for urlconf_module in urlconf_modules:
        urlconf = __import__(urlconf_module, {}, {}, ['urlpatterns'])
        urlpatterns += get_urlpatterns_from_module(urlconf.urlpatterns)
        print(urlpatterns)
    return urlpatterns

def get_urlpatterns_from_module(urlpatterns):
    urlpatterns_list = []

    for pattern in urlpatterns:
        if isinstance(pattern, URLResolver):
            urlpatterns_list += get_urlpatterns_from_module(pattern.url_patterns)
        elif isinstance(pattern, URLPattern):
            urlpatterns_list.append(pattern)
    
    return urlpatterns_list

