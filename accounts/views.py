
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from accounts.models import CustomUser
from accounts.serializers import AccountSerializer


class AccountsList(APIView):
    """
    List all accountss, or create a new account.
    """
    def get(self, request, format=None):
        snippets = CustomUser.objects.all()
        serializer = AccountSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
