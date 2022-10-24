from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import DjangoUnicodeDecodeError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account.user.models import (Profile, UserEducation, UserExperience,
                                 UserInterest, UserServices, UserSkill,
                                 UserSocialMedia)

from .utils import decode_uidb64

User = get_user_model()


class UserInterestSerializer(serializers.ModelSerializer):
    ''' User interest serializer '''
    class Meta:
        model = UserInterest
        fields = ('id', 'name')


class UserServicesSerializer(serializers.ModelSerializer):
    ''' User services serializer '''
    class Meta:
        model = UserServices
        fields = ('id', 'name')


class RegistrationSerializer(serializers.ModelSerializer):
    ''' Register user '''

    password1 = serializers.CharField()
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
            'date_joined',
        )
        extra_kwargs = {
            'email': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'blank': 'Email is required',
                    'null': 'Email is required',
                },
                'validators': [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message='Email already exists. Try another email.')
                ],
            },
            'first_name': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'blank': 'First name is required',
                    'null': 'First name is required'
                }
            },
            'last_name': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'blank': 'Last name is required',
                    'null': 'Last name is required'
                }
            },
            'username': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'blank': 'Username is required',
                    'null': 'Username is required'
                },
                'validators': [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message='A user with that username already exists. Try another one.',
                    )
                ],
            },
            'password1': {
                'min_length': 128,
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'blank': 'Password is required',
                    'null': 'Password is required'
                },
                'validators': [validate_password]
            },
            'password2': {
                'min_length': 128,
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'blank': 'Password is required',
                    'null': 'Password is required'
                },
                'validators': [validate_password]
            },
            'date_joined': {
                'read_only': True
            }
        }

    def validate(self, attrs):
        """
        Verifies that the values entered into the password fields match

        NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
        """
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({'password2': _("The two password fields didn't match. Try again.")})
        return attrs

    def create(self, validated_data):
        ''' create user '''
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user


class UserLoginSerializer(TokenObtainPairSerializer):
    ''' User login serializer with token obtain pair '''

    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials'),
        'inactive_account': _('User account is disabled.'),
        'invalid_credentials': _('Unable to login with provided credentials.'),
        'not_verified': _('User is not verified, please confirm your email.')
    }

    def validate(self, attrs):
        ''' validate user '''
        self.user = authenticate(
            username=attrs.get('username'),
            password=attrs.get('password')
        )

        if not self.user:
            raise AuthenticationFailed(
                self.error_messages['invalid_credentials'],
                status.HTTP_401_UNAUTHORIZED
            )

        if not self.user.is_active:
            raise AuthenticationFailed(
                self.error_messages['inactive_account'],
                status.HTTP_406_NOT_ACCEPTABLE
            )

        if not self.user.is_verified:
            raise AuthenticationFailed(
                self.error_messages['not_verified'],
                status.HTTP_401_UNAUTHORIZED
            )

        attrs['user'] = self.user
        refresh = self.get_token(self.user)

        data = {'refresh': str(refresh), 'access': str(refresh.access_token)}

        data['id'] = self.user.id
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['is_verified'] = self.user.is_verified
        data['date_joined'] = self.user.date_joined
        data['is_active'] = self.user.is_active

        return data


class UserSerializer(serializers.ModelSerializer):
    ''' User serializer '''

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'date_joined', 'is_active', 'is_verified')


class UserPasswordChangeSerializer(serializers.ModelSerializer):
    ''' User change password serializer '''

    old_password = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ['old_password', 'password1', 'password2']
        extra_kwargs = {
            'old_password': {
                'min_length': 128,
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'blank': 'Password is required',
                    'null': 'Password is required'
                },
                'validators': [validate_password]
            },
            'password1': {
                'min_length': 128,
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'blank': 'Password is required',
                    'null': 'Password is required'
                },
                'validators': [validate_password]
            },
            'password2': {
                'min_length': 128,
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'blank': 'Password is required',
                    'null': 'Password is required'
                },
                'validators': [validate_password]
            }
        }

        def validate(self, attrs):
            """
            Verifies that the values entered into the password fields match

            NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
            """
            if attrs['password1'] != attrs['password2']:
                raise serializers.ValidationError({'password2': _("The two password fields didn't match. Try again.")})
            return attrs


class UserPasswordResetEmailSerializer(serializers.Serializer):
    ''' request for password rest email serializer '''
    email = serializers.EmailField()

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        ''' email validation '''
        email = attrs.get('email')
        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("User with this email doesn't exists")

        attrs['user'] = user
        return attrs


class UserPasswordResetSerializer(serializers.Serializer):
    ''' password reset confirm serializer '''

    password1 = serializers.CharField()
    password2 = serializers.CharField()

    class Meta:
        fields = ['password1', 'password2']
        extra_fields = {
            'password1': {
                'min_length': 128,
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'blank': 'Password is required',
                    'null': 'Password is required'
                },
                'validators': [validate_password]
            },
            'password2': {
                'min_length': 128,
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'blank': 'Password is required',
                    'null': 'Password is required'
                },
                'validators': [validate_password]
            }
        }

    def validate(self, attrs):
        """
        Verifies that the values entered into the password fields match
        NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
        """
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({'password2': _("The two password fields didn't match. Try again.")})
        try:
            password = attrs.get('password1')
            uidb64 = self.context.get('uidb64')
            token = self.context.get('token')
            ''' decode uidb64 && get user '''
            user = decode_uidb64(uidb64)
            ''' check token '''
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError({'token': _("Token is invalid, please request a new one.")})
            user.set_password(password)
            user.save()
            return attrs

        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError({'token': _("Token is invalid, please request a new one.")})


class CategoryListingField(serializers.RelatedField):
    def to_representation(self, value):
        return value.name


class ProfileSerializer(serializers.ModelSerializer):
    ''' Profile serializer '''
    user_services = serializers.StringRelatedField(many=True, read_only=True)
    user_interest = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('profie_image', 'user')
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"read_only": True},
            "is_visitor": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "is_active": {"read_only": True},
            "is_staff": {"read_only": True},
            "is_superuser": {"read_only": True},
        }


class ProfileImageSerializer(serializers.ModelSerializer):
    ''' Profile update serializer '''

    class Meta:
        model = Profile
        fields = ('user', 'image',)
        read_only_fields = ('user',)


class UpdateUserSerializer(serializers.ModelSerializer):
    ''' Update user serializer '''
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']

        instance.save()

        return instance


class ExperienceSerializer(serializers.ModelSerializer):
    ''' Experience serializer '''
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserExperience
        fields = '__all__'
        read_only_fields = ('user',)

    def validate(self, attrs):
        ''' validate user '''
        user = self.context['request'].user
        attrs['user'] = user
        return attrs


class EducationSerializer(serializers.ModelSerializer):
    ''' Education serializer '''
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserEducation
        fields = '__all__'
        read_only_fields = ('user',)

    def validate(self, attrs):
        ''' validate user '''
        user = self.context['request'].user
        attrs['user'] = user
        return attrs
