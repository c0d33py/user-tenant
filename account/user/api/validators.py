from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class UniqueEmailValidator(object):
    ''' unique email validator '''

    def __init__(self, queryset):
        self.queryset = queryset

    def __call__(self, value):
        if self.queryset.filter(email=value).exists():
            raise serializers.ValidationError(
                _(f'{value} already exists'),
                code='unique'
            )

    def set_context(self, serializer_field):
        self.instance = getattr(serializer_field.parent, 'instance', None)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.queryset == other.queryset and
            self.instance == other.instance
        )


class PasswordMatchValidator(object):
    ''' unique password validator '''

    def __init__(self, password):
        self.password = password

    def __call__(self, value):
        if value != self.password:
            raise serializers.ValidationError(
                _(f'Password does not match'),
                code='password_match'
            )

    def set_context(self, serializer_field):
        self.instance = getattr(serializer_field.parent, 'instance', None)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.password == other.password and
            self.instance == other.instance
        )


class UniquePhoneNumberValidator(object):
    ''' unique phone number validator '''

    def __init__(self, queryset):
        self.queryset = queryset

    def __call__(self, value):
        if self.queryset.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                _(f'{value} already exists'),
                code='unique'
            )

    def set_context(self, serializer_field):
        self.instance = getattr(serializer_field.parent, 'instance', None)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.queryset == other.queryset and
            self.instance == other.instance
        )


''' email not exist validators '''


class EmailNotExistValidator(object):
    ''' email not exist validator '''

    def __init__(self, queryset):
        self.queryset = queryset

    def __call__(self, value):
        if not self.queryset.filter(email=value).exists():
            raise serializers.ValidationError(
                _(f'{value} does not exist'),
                code='not_exist'
            )

    def set_context(self, serializer_field):
        self.instance = getattr(serializer_field.parent, 'instance', None)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.queryset == other.queryset and
            self.instance == other.instance
        )
