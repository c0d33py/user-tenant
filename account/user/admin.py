from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from account.permissions.models import TenantPermissions
from .models.profile import Profile

User = get_user_model()


@admin.register(TenantPermissions)
class PermAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('User'), {'fields': ('user',)}),
        (_('Permissions'), {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
    )
    filter_horizontal = (
        'groups',
        'user_permissions',
    )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
    list_editable = ('is_active',)
    list_filter = ['is_active']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'),
         {'fields': (
             'first_name',
             'last_name',
             'email',
             'user_services',
             'user_interest',
             'is_visitor',
             'is_content_creator',
             'is_expert'
         )}),
        (_('Tenants & Permissions'), {'fields': ('is_active', 'tenants',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-id']
    filter_horizontal = (
        'tenants',
        'user_services',
        'user_interest'
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image', 'phone', 'city']
    fieldsets = (
        (_('Profile'), {'fields': ('user', 'image',)}),
        (_('Contact address'),
         {'fields': (
             'birth_date',
             'phone',
             'address_1',
             'address_2',
             'city',
             'state',
             'zip_code',
             'country',
             'website',
         )}),
    )
