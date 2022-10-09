
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated

from accounts.util import BearerTokenAuthentication

from devices.models import Device

from positions.models import PositionPing
from positions.serializers import PositionPingSerializer


class PositionPingView(APIView):
    """
    Manage position pings.
    """
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, device_id, format=None):
        """Show history of position pings"""
        try:
            device = Device.objects.get(device_id=device_id)
            position_pings = PositionPing.objects.filter(account=request.user, device=device)
        
            serializer = PositionPingSerializer(position_pings, many=True)
            response = {
                'success': True,
                'pings': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Device.DoesNotExist:
            response = {
                "success": False,
                "message": "This device does not exist."
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, device_id, format=None):
        """Receive position ping"""
        serializer = PositionPingSerializer(data=request.data, many=True)
        if serializer.is_valid():
            account = request.user
            device = Device.objects.get(device_id=device_id)

            for ping in serializer.validated_data:
                ping.update({
                    'account': account,
                    'device': device,
                })

            _ = serializer.save()

            response = {
                "success": True,
                "message": "Successful position pings"
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            # invalid request data
            response = serializer.errors
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
