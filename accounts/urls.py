from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from accounts import views

urlpatterns = [
    path('', views.AccountsList.as_view()),
    path('verify', views.VerifyView.as_view()),
    path('authenticate', views.AuthenticateAccountView.as_view()),
    path('info', views.AccountView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
