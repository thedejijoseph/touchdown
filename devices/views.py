
from django.template import loader
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class DeviceInfoView(APIView):
    """
    Identify and manage a device.
    """

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        pass

class DeviceLocationView(APIView):
    """
    Manage device locations.
    """

    def post(self, request, format=None):
        pass
