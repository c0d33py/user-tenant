import jwt
import pyotp
# from utils import Util
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.encoding import smart_str, smart_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.urls import reverse
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserCreateSerializer, UserSerializerWithToken


'''models'''
User = get_user_model()


class RequestPasswordResetEmail(generics.GenericAPIView):
    ''' Request password reset email '''
    serializer_class = UserSerializer

    def post(self, request):
        ''' Request password reset email '''
        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            password_reset_url = 'http://localhost:3000/reset-password/' + uidb64 + '/' + token
            email_body = 'Hi, ' + user.username + ' Please use link below to reset your password    ' + password_reset_url + ' Thanks'  # noqa E501 pylint: disable=line-too-long
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reset your password'}  # noqa E501 pylint: disable=line-too-long
            Util.send_email(data)

        return Response({'success': 'We have sent you a link to reset your password'},
                        status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    ''' email verification '''
    serializer_class = UserSerializer

    def get(self, request, uidb64, token):
        ''' email verification '''
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success': True, 'message': 'Credentials Valid',
                             'uidb64': uidb64, 'token': token},
                            status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)


''' SetNewPassword serializer '''


class SetNewPasswordAPIView(generics.GenericAPIView):
    ''' Set new password '''
    serializer_class = UserSerializer

    def patch(self, request):
        ''' Set new password '''
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'},
                        status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    ''' Change password '''
    serializer_class = UserSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        ''' Change password '''
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        ''' Change password '''
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"status": "password set"},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProfileView(generics.UpdateAPIView):
    ''' Update profile '''
    serializer_class = UserSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        ''' Update profile '''
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        ''' Update profile '''
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.object.email = serializer.data.get("email")
            self.object.username = serializer.data.get("username")
            self.object.save()
            return Response({"status": "profile updated"},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProfilePictureView(generics.UpdateAPIView):
    ''' Update profile picture '''
    serializer_class = UserSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        ''' Update profile picture '''
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        ''' Update profile picture '''
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.object.profile_picture = serializer.data.get("profile_picture")
            self.object.save()
            return Response({"status": "profile picture updated"},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ''' two factor authentication '''
class TwoFactorAuthView(generics.GenericAPIView):
    ''' Two factor authentication '''
    serializer_class = TwoFactorAuthSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        ''' Two factor authentication '''
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        token = serializer.data.get('token')
        totp = pyotp.TOTP(user.otp_secret_key)
        if totp.verify(token):
            return Response({'status': 'Token is valid'}, status=status.HTTP_200_OK)
        return Response({'status': 'Token is invalid'}, status=status.HTTP_400_BAD_REQUEST)


class TwoFactorAuthSetupView(generics.GenericAPIView):
    ''' Two factor authentication setup '''
    serializer_class = TwoFactorAuthSetupSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        ''' Two factor authentication setup '''
        user = request.user
        totp = pyotp.TOTP(user.otp_secret_key)
        qr_code = totp.provisioning_uri(user.email, issuer_name='Django REST API')
        return Response({'qr_code': qr_code}, status=status.HTTP_200_OK)


class TwoFactorAuthDisableView(generics.GenericAPIView):
    ''' Two factor authentication disable '''
    serializer_class = TwoFactorAuthDisableSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        ''' Two factor authentication disable '''
        user = request.user
        user.otp_secret_key = None
        user.save()
        return Response({'status': 'Two factor authentication disabled'}, status=status.HTTP_200_OK)


class TwoFactorAuthResetView(generics.GenericAPIView):
    ''' Two factor authentication reset '''
    serializer_class = TwoFactorAuthResetSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        ''' Two factor authentication reset '''
        user = request.user
        user.otp_secret_key = pyotp.random_base32()
        user.save()
        return Response({'status': 'Two factor authentication reset'}, status=status.HTTP_200_OK)


class TwoFactorAuthVerifyView(generics.GenericAPIView):
    ''' Two factor authentication verify '''
    serializer_class = TwoFactorAuthVerifySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        ''' Two factor authentication verify '''
        user = request.user
        token = request.data.get('token')
        totp = pyotp.TOTP(user.otp_secret_key)
        if totp.verify(token):
            return Response({'status': 'Token is valid'}, status=status.HTTP_200_OK)
        return Response({'status': 'Token is invalid'}, status=status.HTTP_400_BAD_REQUEST)


''' password reset '''


class PasswordResetView(generics.GenericAPIView):
    ''' Password reset '''
    serializer_class = PasswordResetSerializer

    def post(self, request):
        ''' Password reset '''
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(request).domain
        relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uid, 'token': token})
        absurl = 'http://' + current_site + relative_link
        email_body = 'Hi ' + user.username + ' Use link below to reset your password \n' + absurl + ' \n' + 'Regards, \n' + 'Django REST API'  # noqa E501 pylint: disable=line-too-long
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reset your password'}
        Util.send_email(data)
        return Response({'status': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    ''' Password reset confirm '''
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token):
        ''' Password reset confirm '''
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.data.get('password')
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)  # noqa E501 pylint: disable=line-too-long
        user.set_password(password)
        user.save()
        return Response({'status': 'Password reset success'}, status=status.HTTP_200_OK)


''' email verification '''


class EmailVerificationView(generics.GenericAPIView):
    ''' Email verification '''
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        ''' Email verification '''
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class RequestEmailVerificationView(generics.GenericAPIView):
    ''' Request email verification '''
    serializer_class = RequestEmailVerificationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        ''' Request email verification '''
        user = request.user
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        absurl = 'http://' + current_site + relative_link + '?token=' + str(token)
        email_body = 'Hi ' + user.username + ' Use link below to verify your email \n' + absurl  # noqa E501 pylint: disable=line-too-long
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email'}
        Util.send_email(data)
        return Response({'status': 'We have sent you a link to verify your email'}, status=status.HTTP_200_OK)


''' email verification link expired '''


class EmailVerificationLinkExpiredView(generics.GenericAPIView):
    ''' Email verification link expired '''
    serializer_class = EmailVerificationLinkExpiredSerializer

    def get(self, request):
        ''' Email verification link expired '''
        return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)


''' resend email verification '''


class ResendEmailVerificationView(generics.GenericAPIView):
    ''' Resend email verification '''
    serializer_class = ResendEmailVerificationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        ''' Resend email verification '''
        user = request.user
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        absurl = 'http://' + current_site + relative_link + '?token=' + str(token)
        email_body = 'Hi ' + user.username + ' Use link below to verify your email \n' + absurl  # noqa E501 pylint: disable=line-too-long
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email'}
        Util.send_email(data)
        return Response({'status': 'We have sent you a link to verify your email'}, status=status.HTTP_200_OK)


''' generate google authenication code '''


class GenerateGoogleAuthenicationCodeView(generics.GenericAPIView):
    ''' Generate google authenication code '''
    serializer_class = GenerateGoogleAuthenicationCodeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        ''' Generate google authenication code '''
        user = request.user
        totp = pyotp.TOTP(user.google_authenication_code)
        return Response({'status': totp.now()}, status=status.HTTP_200_OK)


''' google authenication '''


class GoogleAuthenicationView(generics.GenericAPIView):
    ''' Google authenication '''
    serializer_class = GoogleAuthenicationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        ''' Google authenication '''
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        totp = pyotp.TOTP(user.google_authenication_code)
        if totp.verify(serializer.data.get('google_authenication_code')):
            return Response({'status': 'Google authenication success'}, status=status.HTTP_200_OK)
        return Response({'error': 'Google authenication failed'}, status=status.HTTP_400_BAD_REQUEST)


''' google authenicator app '''


class GoogleAuthenicatorAppView(generics.GenericAPIView):
    ''' Google authenicator app '''
    serializer_class = GoogleAuthenicatorAppSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        ''' Google authenicator app '''
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.google_authenication_code = serializer.data.get('google_authenication_code')
        user.save()
        return Response({'status': 'Google authenicator app success'}, status=status.HTTP_200_OK)
