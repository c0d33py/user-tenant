from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import DjangoUnicodeDecodeError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, filters, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from account.user.models import (  # UserPortfolio,; UserSkill,; UserLanguage,; UserAward,; UserCertificate
    Profile, UserEducation, UserExperience, UserInterest, UserServices)

from .email_helper import send_activation_email, send_reset_password_email
from .serializers import (EducationSerializer, ExperienceSerializer,
                          ProfileImageSerializer, ProfileSerializer,
                          RegistrationSerializer, UserInterestSerializer,
                          UserLoginSerializer, UserPasswordChangeSerializer,
                          UserPasswordResetEmailSerializer,
                          UserPasswordResetSerializer, UserSerializer,
                          UserServicesSerializer)
from .utils import decode_uidb64

'''models'''
User = get_user_model()


############################################
'''User AUTHENTICATION'''
############################################


class UserAPIView(APIView):
    ''' User views api'''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserInterestAPIView(generics.ListAPIView):
    ''' get user interest '''
    serializer_class = UserInterestSerializer
    permission_classes = [permissions.AllowAny, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        ''' get queryset '''
        return UserInterest.objects.all()


class UserServicesAPIView(generics.ListAPIView):
    ''' get user services '''
    serializer_class = UserServicesSerializer
    permission_classes = [permissions.AllowAny, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        ''' get queryset '''
        return UserServices.objects.all()


class UserRegisterAPIView(generics.GenericAPIView):
    ''' Register user '''

    authentication_classes = []
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_activation_email(user, self.request)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })


class UserEmailVerifyAPIView(generics.GenericAPIView):
    ''' verify user account api view '''

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    token_generator = PasswordResetTokenGenerator()

    def get(self, request, uidb64, token):
        ''' handle get request '''
        try:
            user = decode_uidb64(uidb64)
            if not self.token_generator.check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)
            if user.is_verified:
                return Response({'error': 'Email is already verified'},
                                status=status.HTTP_401_UNAUTHORIZED)
            user.is_verified = True
            user.save()
            return Response({'message': 'Successfully activated'},
                            status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            if not isinstance('user', User):
                return Response({'error': 'Invalid token'},
                                status=status.HTTP_401_UNAUTHORIZED)


class UserLoginAPIView(TokenObtainPairView):
    ''' user login api view with jwt token '''
    serializer_class = UserLoginSerializer

    ''' return user data with token '''

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        return Response({
            'user': serializer.validated_data,
            'message': f'{username} Authenticated Successfully!',
        })


class UserPasswordChangeAPIView(generics.UpdateAPIView):
    ''' change password api view '''

    serializer_class = UserPasswordChangeSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        ''' get user object '''
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        ''' update user password '''
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"message": ["Your old password was entered incorrectly. Please enter it again.."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("password1"))
            self.object.save()
            return Response({"message": "Your Password has been Updated Successfully!"},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


############################################
'''User FORGOT PASSWORD API'''
############################################


class RequestPasswordResetEmail(generics.GenericAPIView):
    '''Request password reset email'''

    authentication_classes = []
    serializer_class = UserPasswordResetEmailSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        ''' SetNewPassword serializer '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        send_reset_password_email(user, self.request)
        return Response(
            {'message': 'We have sent you a link to reset your password'},
            status=status.HTTP_200_OK
        )


class UserPasswordResetAPIView(generics.GenericAPIView):
    ''' reset password api view '''
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserPasswordResetSerializer

    def post(self, request, uidb64, token, format=None):
        serializer = self.get_serializer(data=request.data, context={'uidb64': uidb64, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    ''' check password token api view '''

    permission_classes = (permissions.AllowAny,)

    def get(self, request, uidb64, token):
        try:
            user = decode_uidb64(uidb64)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)


############################################
'''User Profile'''
############################################


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    ''' user profile api view '''

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer
    model = Profile

    def get_object(self, queryset=None):
        ''' get user profile '''
        return Profile.objects.get(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        ''' get user profile '''
        self.object = self.get_object()
        serializer = self.get_serializer(self.object)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return self.update(request, *args, **kwargs)

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProfileSerializer
        return ProfileSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]


class UserProfilePictureUpdateAPIView(generics.UpdateAPIView):
    ''' Update profile picture '''

    serializer_class = ProfileImageSerializer
    permission_classes = (permissions.IsAuthenticated,)
    model = Profile

    def get_object(self, queryset=None):
        ''' Update profile picture '''
        return Profile.objects.get(user=self.request.user)

    def update(self, request, *args, **kwargs):
        ''' Update profile picture '''
        self.object = self.get_object()
        serializer = self.get_serializer(self.object, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProfileImageSerializer
        return ProfileImageSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]


#######################
''' UserExperience '''
#######################


class UserExperienceAPIView(generics.ListCreateAPIView):
    ''' UserExperience APIView according to user '''

    serializer_class = ExperienceSerializer
    permission_classes = (permissions.IsAuthenticated,)
    model = UserExperience

    def get_queryset(self):
        ''' get user experience '''
        return UserExperience.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        ''' create user experience '''
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ExperienceSerializer
        return ExperienceSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]


class UserExperienceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    ''' UserExperienceDetail APIView according to user '''

    serializer_class = ExperienceSerializer
    permission_classes = (permissions.IsAuthenticated,)
    model = UserExperience

    def get_queryset(self):
        ''' get user experience '''
        return UserExperience.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        ''' get user experience '''
        return UserExperience.objects.get(id=self.kwargs['pk'])

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ExperienceSerializer
        return ExperienceSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]


#######################
''' UserEducation '''
#######################


class UserEducationAPIView(generics.ListCreateAPIView):
    ''' UserEducation APIView according to user '''

    serializer_class = EducationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    model = UserEducation

    def get_queryset(self):
        ''' get user education '''
        return UserEducation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        ''' create user education '''
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EducationSerializer
        return EducationSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            instance = self.get_object()
            # not permitted check
            if instance.user is not self.request.user:
                raise exceptions.PermissionDenied()
            return True
        # Write permissions are only allowed to the owner of the blog.
        return obj.user == request.user


class UserEducationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    ''' UserEducationDetail APIView according to user '''

    serializer_class = EducationSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    model = UserEducation

    def get_queryset(self):
        ''' get user education '''
        return UserEducation.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        ''' get user education '''
        return UserEducation.objects.get(id=self.kwargs['pk'])

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EducationSerializer
        return EducationSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    ''' only owner can update or delete '''

    def perform_update(self, serializer):
        ''' update user education '''
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        ''' delete user education '''
        instance.delete()


############################################
''' User CRUD'''
############################################


class UserListView(generics.ListAPIView):
    ''' List users '''
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['username', 'email']
    search_fields = ['username', 'email']
    ordering_fields = ['username', 'email']


class UserDetailView(generics.RetrieveAPIView):
    ''' User detail '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'id'


class UserUpdateView(generics.UpdateAPIView):
    ''' Update user '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'id'


class UserDeleteView(generics.DestroyAPIView):
    ''' Delete user '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'id'


class UserCreateView(generics.CreateAPIView):
    ''' Create user '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'id'
