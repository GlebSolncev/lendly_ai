from django.shortcuts import redirect

from base.models import Setting, Contact


def context_controller(request):
    settings = Setting.get_settings()
    contacts = Contact.objects.filter()

    context = {
        'settings': settings,
        'contacts': contacts,
    }

    return context