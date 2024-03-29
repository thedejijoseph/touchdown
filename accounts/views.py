

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from accounts.models import CustomUser, AuthCode
from accounts.serializers import AccountSerializer, VerifyAccountSerializer, AuthenticateAccountSerializer

from accounts.util import BearerTokenAuthentication
from accounts.util import render_email_verification_template_html, render_email_verification_template_text
from accounts.mailer import send_email


class AccountsList(APIView):
    """
    List all accountss, or create a new account.
    """
    def get(self, request, format=None):
        accounts = CustomUser.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()

            create_auth_code_object = AuthCode.objects.create(account=account)
            auth_code = create_auth_code_object.auth_code

            body_text = render_email_verification_template_text({"auth_code": auth_code})
            body_html = render_email_verification_template_html({"auth_code": auth_code})

            email_payload = {
                "to": serializer.validated_data['email'],
                "subject": "Verify your email address",
                "plain_text": body_text,
                "html": body_html,
            }

            response = {}
            response.update(serializer.data)

            try:
                email = send_email(**email_payload)
                if email.status_code == 200:
                    response.update(
                        {"message": "User registered. Verification email is on its way."}
                    )
                else:
                    response.update(
                        {"message": "User registered. Failed to send verification email."}
                    )
            except:
                # log critical failure
                pass
                
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyView(APIView):
    """
    Send auth codes.
    """
    
    def post(self, request, format=None):
        serializer = VerifyAccountSerializer(data=request.data)
        if serializer.is_valid():
            try:
                account = CustomUser.objects.get(email=serializer.validated_data['email'])
            except:
                response = [
                    {
                        "email": "A user with that email address does not exist."
                    }
                ]
                return Response(response, status=status.HTTP_400_BAD_REQUEST)


            auth_code_object = AuthCode.objects.get_or_create(account=account)
            auth_code = auth_code_object[0].auth_code

            body_text = render_email_verification_template_text({"auth_code": auth_code})
            body_html = render_email_verification_template_html({"auth_code": auth_code})

            email_payload = {
                "to": serializer.validated_data['email'],
                "subject": "Verify your email address",
                "plain_text": body_text,
                "html": body_html,
            }

            response = {}

            try:
                email = send_email(**email_payload)
                if email.status_code == 200:
                    response.update(
                        {"message": "Verification email is on its way."}
                    )
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    response.update(
                        {"message": "Failed to send verification email."}
                    )
                    return Response(response, status=status.HTTP_200_OK)
            except:
                # log critical failure
                raise
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthenticateAccountView(ObtainAuthToken):
    """
    Authenticate created accounts.
    """

    def post(self, request, format=None):
        serializer = AuthenticateAccountSerializer(data=request.data)
        if serializer.is_valid():
            try:
                account = CustomUser.objects.get(email=serializer.validated_data['email'])
            except:
                response = [
                    {
                        "email": "A user with that email address does not exist."
                    }
                ]
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
                
            try:
                received_auth_code = serializer.validated_data['auth_code']

                auth_code_object = AuthCode.objects.get(account=account)
                stored_auth_code = auth_code_object.auth_code
                
                if received_auth_code == stored_auth_code:
                    auth_token, _ = Token.objects.get_or_create(user=account)
                    response = {
                        "success": True,
                        "token": auth_token.key,
                        "message": "Authenticated successfully"
                    }
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    response = [
                    {
                        "auth_code": "Invalid authorization code. Request verification email."
                    }
                ]
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            except:
                response = [
                    {
                        "email": "Authorization has not been created for this account. Request verification email."
                    }
                ]
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        else:
            # invalid request data
            response = serializer.errors
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class AccountView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        response = {
            "email": request.user.email,
        }
        return Response(response, status=status.HTTP_200_OK)
