
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from positions import views

urlpatterns = [
    path('pings/<uuid:device_id>', views.PositionPingView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
