
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

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

    def clean(self):
        cleaned_data = super(UserRegistration, self).clean()
        username = cleaned_data.get('username')

        # if len(username) < 6:
        #     self.add_error('username', 'Username must contain at least 6 character.')


# class UserProfileUpdateForm(UserRegistration):
#     def __init__(self, *args, **kwargs):
#         super(UserRegistration, self).__init__(*args, **kwargs)
#         self.fields['is_visitor'].disabled = True
#         self.fields['email'].required = True

#     class Meta:
#         model = User
#         fields = [
#             'user_interest',
#             'user_services',
#             'is_visitor',
#             'is_content_creator',
#             'is_expert',
#         ]
#         labels = {
#             'user_interest': 'Your Interest*',
#             'user_services': 'Your Services*',
#             'is_visitor': 'Visitor',
#             'is_content_creator': 'Content Creator',
#             'is_expert': 'Expert',
#         }

#     def clean(self):
#         cleaned_data = super(UserRegistration, self).clean()
#         username = cleaned_data.get('username')

        # if len(username) < 6:
        #     self.add_error('username', 'Username must contain at least 6 character.')
