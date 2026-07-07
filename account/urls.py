from django.urls import path
import account.views as account

urlpatterns = [
    path('login/', account.login, name='login'),
    path('sign-up/', account.sign_up, name='sign_up'),
    path('logout/', account.logout, name='logout'),
    path('reset-password/', account.reset_password, name='reset_password'),
    path('restore-password/',  account.restore_password, name='restore_password'),
]
