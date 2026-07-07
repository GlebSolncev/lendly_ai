from django.contrib.sitemaps import Sitemap
from .utils import get_urlpatterns
from django.urls import reverse
from wagtail.models import Page

class MySitemap(Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        static_urls = ["index", 
                "about","seo_keyword","content_creator","image_generator","logo_generator","car_dealership","display_ads", "ecommerce_sales",
                 "education",
                 "finance",
                 "games_and_entertainment",
                 "health_and_beauty",
                 "insurance",
                 "lead_generation",
                 "marketing_and_advertising",
                 "real_estate",
                 "retargeting",
                 "search_ads",
                 "social_ads",
                 "software_and_tech",
                 "sports_and_events",
        ]

        # Query all live Wagtail pages
        wagtail_pages = Page.objects.live()

        # Combine static URLs and live Wagtail pages
        return static_urls + list(wagtail_pages)

    def location(self, item):
        # Check if the item is a string (static URL) or a Wagtail Page object
        if isinstance(item, str):
            # For static URLs, use reverse to generate the URL
            return reverse(item)
        else:
            # For Wagtail Page objects, use get_url to generate the URL
            return item.get_url()