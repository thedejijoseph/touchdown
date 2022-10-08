from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from devices import views

urlpatterns = [
    path('info', views.DeviceInfoView.as_view()),
    path('location', views.DeviceLocationView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
