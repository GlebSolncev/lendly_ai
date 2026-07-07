from django.urls import path
import user.views as user

urlpatterns = [
    path('account/', user.account, name='account'),
]