from django.contrib import admin

from base.models import Setting, Faq, Contact, Page, subscriberList

admin.site.register(Setting)
admin.site.register(Faq)
admin.site.register(Contact)
admin.site.register(Page)
admin.site.register(subscriberList)