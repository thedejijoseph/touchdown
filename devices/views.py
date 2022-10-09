
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated

from accounts.util import BearerTokenAuthentication

from devices.models import Device
from devices.serializers import DeviceInfoSerializer


class DevicesOnAccountView(APIView):
    """
    Identify and manage a device.
    """
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """List all devices on this account"""
        devices = Device.objects.filter(account=request.user)
        serializer = DeviceInfoSerializer(devices, many=True)

        response = {
            "success": True,
            "devices": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """Add new device to an account"""
        serializer = DeviceInfoSerializer(data=request.data)
        if serializer.is_valid():
            account = request.user
            serializer.validated_data.update({
                'account': account
            })
            device = serializer.save()

            response = {
                "success": True,
                "device_id": device.device_id,
                "message": "Added device to account successfully"
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            # invalid request data
            response = serializer.errors
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class DeviceInfoView(APIView):
    """
    View and manage a single device
    """
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, device_id, format=None):
        """View info on a single device"""
        try:
            accounts_devices = Device.objects.filter(account=request.user)
            try:
                device_queryset = accounts_devices.filter(device_id=device_id)
                if len(device_queryset) > 0:
                    device = list(device_queryset)[0]
                    serializer = DeviceInfoSerializer(device)
                    response = {
                        'success': True,
                        'device': serializer.data
                    }
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    raise Device.DoesNotExist
            except Device.DoesNotExist:
                response = {
                    "success": False,
                    "message": "Device is not on this account"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Device.DoesNotExist:
            response = {
                "success": False,
                "message": "No devices added to this account"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, device_id, format=None):
        """Update info on a single device"""
        try:
            device = Device.objects.get(device_id=device_id)
            if device.account == request.user:
                serializer = DeviceInfoSerializer(data=request.data)
                if serializer.is_valid():
                    device_update = serializer.update(device, serializer.validated_data)
                    device_update.save()

                    updated_device = DeviceInfoSerializer(device_update)

                    response = {
                        'success': True,
                        'device': updated_device.data
                    }
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    # invalid request data
                    response = serializer.errors
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {
                    "success": False,
                    "message": "Device does not belong to this account"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Device.DoesNotExist:
            response = {
                "success": False,
                "message": "This device does not exist"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)



class DeviceLocationView(APIView):
    """
    Manage device locations.
    """

    def post(self, request, format=None):
        pass
