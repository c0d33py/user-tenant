
from .serializers import ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer
from .models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import generics, status
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


def send_activate_token_email(user, domain):
    '''
    Send activate token to user email
    Args:
        user (object): The user instance
        domain (str): The current domain
    '''
    uid, token = account_activation_token.make_token(user)
    url = reverse('activate', kwargs={'uidb64': uid, 'token': token})
    activate_url = 'http://' + domain + url
    email_body = 'Hi ' + user.username + ' Please use this link to verify your email \n' + activate_url
    email_data = {
        'subject': 'Verify your email',
        'body': email_body,
        'email_from': settings.EMAIL_HOST_USER,
        'email_to': [user.email]
    }
    Util.send_email(email_data)


''' check email link expire '''


def is_token_expire(token):
    '''
    Check if the token is expire
    Args:
        token (str): The token
    Returns:
        bool: True if token is expire
    '''
    try:
        payload = jwt.decode(token, settings.SECRET_KEY)
        return payload['exp'] < time.time()
    except jwt.ExpiredSignatureError:
        return True


''' UserPasswordResetAPIView '''


class UserPasswordResetAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data.get('email', '')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            domain = get_current_site(request=request).domain
            link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            reset_url = 'http://' + domain + link
            email_body = 'Hello, \n Use link below to reset your password  \n' + reset_url
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reset your password'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


'''SetNewPasswordSerializer'''
