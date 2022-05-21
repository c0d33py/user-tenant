
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


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
    def __init__(self, *args, **kwargs):
        super(UserRegistration, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = [
            'email',
            'password1',
            'password2',
        ]
