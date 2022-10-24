
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from .models import Profile

User = get_user_model()


class UserAdminCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = '__all__'


class UserAdminChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = '__all__'


class UserTenantConfigForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['tenants']


class UserRegistration(UserCreationForm):

    email_validator = RegexValidator(
        regex='@(gmail.com)$',
        message='Only Gmail user are allowed to register.',
        code='invalid_email',
    )
    email = forms.EmailField(validators=[email_validator])

    def __init__(self, *args, **kwargs):
        super(UserRegistration, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]
        labels = {'email': 'email*', }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 6:
            raise forms.ValidationError('Username must contain at least 6 character.')
        return username


class UserUpdateForm(forms.ModelForm):
    email_validator = RegexValidator(
        regex='@(gmail.com)$',
        message='Only Gmail user are allowed to register.',
        code='invalid_email',
    )
    email = forms.EmailField(validators=[email_validator])

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
        ]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 6:
            raise forms.ValidationError('Username must contain at least 6 character.')
        return username


class UserProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']
        labels = {
            'user_interest': 'Your Interest*',
            'user_services': 'Your Services*',
            'is_visitor': 'Visitor',
            'is_content_creator': 'Content Creator',
            'is_expert': 'Expert',
        }
